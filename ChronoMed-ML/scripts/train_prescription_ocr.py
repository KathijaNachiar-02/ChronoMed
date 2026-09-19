import torch
import json
from pathlib import Path

from PIL import Image
from datasets import Dataset

from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel,
    Seq2SeqTrainer,
    ViTImageProcessor,
    RobertaTokenizer,
    Seq2SeqTrainingArguments,
)


# ============================================================
# SETTINGS
# ============================================================

MODEL_NAME = "microsoft/trocr-base-handwritten"

DATA_ROOT = Path("datasets/prescription_raw")

OUTPUT_DIR = "models/prescription_ocr"

MAX_LENGTH = 256


# ============================================================
# DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Using device:", device)


# ============================================================
# LOAD DATASET
# ============================================================

def load_prescription_split(split):

    # Hugging Face dataset uses "validation"
    # but downloaded folder is named "val"
    if split == "validation":
        folder = "val"
    else:
        folder = split

    images_dir = DATA_ROOT / folder / "images"
    annotations_dir = DATA_ROOT / folder / "annotations"

    records = []

    image_files = sorted(images_dir.glob("*.png"))

    print()
    print(f"Loading {split} split...")
    print(f"Images found: {len(image_files)}")

    for image_path in image_files:

        # Matching JSON annotation
        annotation_path = (
            annotations_dir / f"{image_path.stem}.json"
        )

        if not annotation_path.exists():

            print(
                f"WARNING: Missing annotation for {image_path.name}"
            )

            continue

        # Read annotation
        with open(
            annotation_path,
            "r",
            encoding="utf-8"
        ) as f:

            annotation = json.load(f)

        records.append(
            {
                "image_path": str(image_path),
                "ground_truth": annotation["ground_truth"],
            }
        )

    print(
        f"{split} records loaded: {len(records)}"
    )

    return Dataset.from_list(records)


# ============================================================
# LOAD TRAINING + VALIDATION DATA
# ============================================================

train_dataset = load_prescription_split("train")

val_dataset = load_prescription_split("validation")


print()
print("=" * 60)
print("DATASET SUMMARY")
print("=" * 60)

print("Training samples:", len(train_dataset))
print("Validation samples:", len(val_dataset))


# ============================================================
# LOAD TROCR PROCESSOR
# ============================================================

print()
print("=" * 60)
print("Loading TrOCR processor...")
print("=" * 60)


# Load image processor separately
image_processor = ViTImageProcessor.from_pretrained(
    MODEL_NAME
)


# Load Roberta tokenizer separately
# This avoids the tokenizer backend issue encountered earlier
tokenizer = RobertaTokenizer.from_pretrained(
    MODEL_NAME
)


# Create TrOCR processor manually
processor = TrOCRProcessor(
    image_processor=image_processor,
    tokenizer=tokenizer
)


print("Processor loaded successfully.")


# ============================================================
# LOAD TROCR MODEL
# ============================================================

print()
print("=" * 60)
print("Loading TrOCR model...")
print("=" * 60)


model = VisionEncoderDecoderModel.from_pretrained(
    MODEL_NAME
)


# ------------------------------------------------------------
# Token configuration
# ------------------------------------------------------------

model.config.decoder_start_token_id = (
    processor.tokenizer.cls_token_id
)

model.config.pad_token_id = (
    processor.tokenizer.pad_token_id
)

model.config.eos_token_id = (
    processor.tokenizer.sep_token_id
)


# IMPORTANT:
# Generation parameters must be stored in generation_config,
# NOT model.config.
#
# This fixes the checkpoint-saving error:
#
# ValueError:
# Some generation parameters are set in the model config.
# Generation parameters found: {'max_length': 256}
# ------------------------------------------------------------

model.generation_config.decoder_start_token_id = (
    processor.tokenizer.cls_token_id
)

model.generation_config.pad_token_id = (
    processor.tokenizer.pad_token_id
)

model.generation_config.eos_token_id = (
    processor.tokenizer.sep_token_id
)

model.generation_config.max_length = MAX_LENGTH


print("Model loaded successfully.")


# ============================================================
# PREPROCESS FUNCTION
# ============================================================

def preprocess(example):

    # --------------------------------------------------------
    # Load prescription image
    # --------------------------------------------------------

    image = Image.open(
        example["image_path"]
    ).convert("RGB")


    # --------------------------------------------------------
    # Convert image to pixel values
    # --------------------------------------------------------

    pixel_values = processor(
        images=image,
        return_tensors="pt"
    ).pixel_values.squeeze(0)


    # --------------------------------------------------------
    # Convert ground-truth text into token IDs
    # --------------------------------------------------------

    labels = processor.tokenizer(
        example["ground_truth"],
        padding="max_length",
        max_length=MAX_LENGTH,
        truncation=True,
    ).input_ids


    # --------------------------------------------------------
    # Ignore padding tokens during loss calculation
    # --------------------------------------------------------

    labels = [
        token
        if token != processor.tokenizer.pad_token_id
        else -100
        for token in labels
    ]


    return {
        "pixel_values": pixel_values,
        "labels": labels,
    }


# ============================================================
# PREPROCESS TRAINING DATA
# ============================================================

print()
print("=" * 60)
print("Preprocessing training dataset...")
print("=" * 60)


train_dataset = train_dataset.map(
    preprocess,
    remove_columns=train_dataset.column_names,
)


print("Training preprocessing completed.")


# ============================================================
# PREPROCESS VALIDATION DATA
# ============================================================

print()
print("=" * 60)
print("Preprocessing validation dataset...")
print("=" * 60)


val_dataset = val_dataset.map(
    preprocess,
    remove_columns=val_dataset.column_names,
)


print("Validation preprocessing completed.")


# ============================================================
# TRAINING CONFIGURATION
# ============================================================

training_args = Seq2SeqTrainingArguments(

    # Model output directory
    output_dir=OUTPUT_DIR,

    # Number of complete passes through training data
    num_train_epochs=5,

    # RTX 3050-friendly batch size
    per_device_train_batch_size=1,

    # Validation batch size
    per_device_eval_batch_size=1,

    # Simulate larger batch size
    gradient_accumulation_steps=8,

    # Learning rate
    learning_rate=5e-5,

    # Regularization
    weight_decay=0.01,

    # Print loss every 10 steps
    logging_steps=10,

    # Evaluate after every epoch
    eval_strategy="epoch",

    # Save checkpoint after every epoch
    save_strategy="epoch",

    # Keep only the latest 2 checkpoints
    save_total_limit=2,

    # Use FP16 on CUDA
    fp16=torch.cuda.is_available(),

    # Generate text during evaluation
    predict_with_generate=True,

    # Disable external reporting
    report_to="none",
)


# ============================================================
# CREATE TRAINER
# ============================================================

trainer = Seq2SeqTrainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=val_dataset,

    processing_class=processor,
)


# ============================================================
# START TRAINING
# ============================================================

print()
print("=" * 60)
print("Starting OCR training...")
print("=" * 60)


trainer.train()


# ============================================================
# SAVE FINAL MODEL
# ============================================================

print()
print("=" * 60)
print("Saving trained model...")
print("=" * 60)


trainer.save_model(
    OUTPUT_DIR
)


processor.save_pretrained(
    OUTPUT_DIR
)


print()
print("=" * 60)
print("Training completed successfully.")
print("Model saved to:", OUTPUT_DIR)
print("=" * 60)