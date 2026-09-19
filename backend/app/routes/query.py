from fastapi import APIRouter

router = APIRouter(
    prefix="/api/query",
    tags=["Q&A"]
)

query_history = []


@router.post("")
def ask_question(query: dict):
    question = query.get("question", "")

    answer = {
        "question": question,
        "answer": "No AI-generated answer is available yet.",
        "status": "needs_review"
    }

    query_history.append(answer)

    return answer


@router.get("/history")
def get_query_history():
    return query_history