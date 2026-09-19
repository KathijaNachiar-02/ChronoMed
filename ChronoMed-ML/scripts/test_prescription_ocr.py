import torch
from pathlib import Path
from PIL import Image

from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel,
    ViTImageProcessor,
    RobertaTokenizer,
)


# ============================================================
# SETTINGS
# ============================================================

MODEL_PATH = "models/prescription_ocr"

TEST_IMAGE_DIR = Path(
    "datasets/prescription_raw/test/images"
)


# ============================================================
# DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Using device:", device)


# ============================================================
# LOAD PROCESSOR
# ============================================================

print()
print("=" * 60)
print("Loading OCR processor...")
print("=" * 60)


image_processor = ViTImageProcessor.from_pretrained(
    MODEL_PATH
)

tokenizer = RobertaTokenizer.from_pretrained(
    MODEL_PATH
)

processor = TrOCRProcessor(
    image_processor=image_processor,
    tokenizer=tokenizer
)

print("Processor loaded successfully.")


# ============================================================
# LOAD MODEL
# ============================================================

print()
print("=" * 60)
print("Loading trained OCR model...")
print("=" * 60)


model = VisionEncoderDecoderModel.from_pretrained(
    MODEL_PATH
)

model.to(device)

model.eval()

print("Model loaded successfully.")


# ============================================================
# FIND TEST IMAGES
# ============================================================

image_files = sorted(
    TEST_IMAGE_DIR.glob("*.png")
)

print()
print("Test images found:", len(image_files))


if len(image_files) == 0:

    raise FileNotFoundError(
        f"No PNG images found in: {TEST_IMAGE_DIR}"
    )


# ============================================================
# SELECT FIRST TEST IMAGE
# ============================================================

image_path = image_files[0]

print()
print("Testing image:")
print(image_path)


# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(
    image_path
).convert("RGB")


# ============================================================
# PREPROCESS IMAGE
# ============================================================

pixel_values = processor(
    images=image,
    return_tensors="pt"
).pixel_values


pixel_values = pixel_values.to(device)


# ============================================================
# GENERATE OCR TEXT
# ============================================================

print()
print("=" * 60)
print("Running OCR...")
print("=" * 60)


with torch.no_grad():

    generated_ids = model.generate(
        pixel_values,
        max_length=256,
    )


# ============================================================
# DECODE RESULT
# ============================================================

generated_text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)[0]


# ============================================================
# DISPLAY RESULT
# ============================================================

print()
print("=" * 60)
print("OCR RESULT")
print("=" * 60)

print(generated_text)

print("=" * 60)