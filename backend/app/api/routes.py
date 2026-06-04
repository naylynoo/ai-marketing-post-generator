import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.history import GeneratedHistory
from app.schemas.generation import GenerateRequest, GenerateResponse, HistoryItem, HistoryListResponse
from app.services.ai_generator import generate_marketing_copy

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_endpoint(request: GenerateRequest, session: Session = Depends(get_session)) -> GenerateResponse:
    try:
        ai_result = await generate_marketing_copy(request.model_dump())
    except Exception as exc:  # noqa: BLE001
        logger.exception("AI generation failed")
        raise HTTPException(status_code=500, detail="AI generation failed") from exc

    history = GeneratedHistory(
        product_name=request.product_name,
        product_description=request.product_description,
        target_audience=request.target_audience,
        platform_type=request.platform_type,
        caption=ai_result["caption"],
        short_ad_text=ai_result["short_ad_text"],
        hashtags=ai_result.get("hashtags", []),
        email_subject=ai_result["email_subject"],
        cta=ai_result["cta"],
    )

    session.add(history)
    session.commit()
    session.refresh(history)

    return GenerateResponse(
        id=history.id,
        caption=history.caption,
        short_ad_text=history.short_ad_text,
        hashtags=history.hashtags,
        email_subject=history.email_subject,
        cta=history.cta,
        created_at=history.created_at,
    )


@router.get("/history", response_model=HistoryListResponse)
def list_history(session: Session = Depends(get_session)) -> HistoryListResponse:
    statement = select(GeneratedHistory).order_by(GeneratedHistory.created_at.desc())
    results: List[GeneratedHistory] = session.exec(statement).all()
    items = [
        HistoryItem(
            id=row.id,
            product_name=row.product_name,
            product_description=row.product_description,
            target_audience=row.target_audience,
            platform_type=row.platform_type,
            caption=row.caption,
            short_ad_text=row.short_ad_text,
            hashtags=row.hashtags,
            email_subject=row.email_subject,
            cta=row.cta,
            created_at=row.created_at,
        )
        for row in results
    ]
    return HistoryListResponse(items=items)


@router.delete("/history/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(item_id: int, session: Session = Depends(get_session)) -> None:
    instance = session.get(GeneratedHistory, item_id)
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found")
    session.delete(instance)
    session.commit()
