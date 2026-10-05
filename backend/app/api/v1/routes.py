from concurrent.futures import ThreadPoolExecutor
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password
from app.db.session import get_db
from app.models import Output, Transformation, User
from app.schemas.common import (
    OutputFormat,
    OutputPayload,
    TokenResponse,
    TransformRequest,
    TransformResponse,
    UserCreate,
    UserRead,
)
from app.services.generators import generate_for_format
from app.services.input_processing import normalize_input
from app.services.router import select_model

router = APIRouter(prefix="/api/v1")


def _quality_score(fmt: OutputFormat, content: dict[str, Any]) -> float:
    if fmt == OutputFormat.linkedin:
        post_len = len(content.get("post_text", ""))
        hashtags = len(content.get("hashtags", []))
        return 85.0 if post_len <= 300 and 3 <= hashtags <= 5 else 68.0
    if fmt == OutputFormat.twitter:
        tweets = content.get("tweets", [])
        return 82.0 if all(len(t.get("text", "")) <= 280 for t in tweets) else 65.0
    if fmt == OutputFormat.executive_summary:
        return 80.0 if content.get("sections") and content.get("markdown") else 60.0
    return 78.0 if content.get("script") and content.get("subtitles") else 60.0


@router.post("/auth/signup", response_model=UserRead)
def signup(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    user = User(email=payload.email, hashed_password=hash_password(payload.password), subscription_tier="free")
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(id=user.id, email=user.email, subscription_tier=user.subscription_tier, created_at=user.created_at)


@router.post("/auth/token", response_model=TokenResponse)
def issue_token(payload: UserCreate, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None:
        user = User(email=payload.email, hashed_password=hash_password(payload.password), subscription_tier="free")
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.post("/transform", response_model=TransformResponse)
def transform(payload: TransformRequest, db: Session = Depends(get_db)) -> TransformResponse:
    normalized = normalize_input(payload.content, payload.input_type.value)
    chosen_model = select_model(payload.parameters.quality_cost_balance)

    transformation = Transformation(
        user_id=1,
        input_content=normalized["normalized_content"],
        input_type=payload.input_type.value,
        parameters=payload.parameters.model_dump(),
        source_metadata={**normalized["metadata"], "selected_model": chosen_model.model_name},
        status="processing",
    )
    db.add(transformation)
    db.commit()
    db.refresh(transformation)

    outputs: list[OutputPayload] = []

    def _generate(fmt: OutputFormat) -> tuple[OutputFormat, dict[str, Any], float]:
        content = generate_for_format(fmt, transformation.input_content, payload.parameters)
        score = _quality_score(fmt, content)
        return fmt, content, score

    with ThreadPoolExecutor(max_workers=max(1, len(payload.output_formats))) as executor:
        for fmt, content, score in executor.map(_generate, payload.output_formats):
            out = Output(
                transformation_id=transformation.id,
                format_type=fmt.value,
                content=content,
                quality_score=score,
            )
            db.add(out)
            outputs.append(OutputPayload(format_type=fmt, content=content, quality_score=score))

    transformation.status = "completed"
    db.commit()

    return TransformResponse(transformation_id=transformation.id, status=transformation.status, outputs=outputs)


@router.get("/transform/{transformation_id}", response_model=TransformResponse)
def get_transform(transformation_id: int, db: Session = Depends(get_db)) -> TransformResponse:
    transformation = db.get(Transformation, transformation_id)
    if transformation is None:
        raise HTTPException(status_code=404, detail="Transformation not found")
    outputs = db.scalars(select(Output).where(Output.transformation_id == transformation_id)).all()
    return TransformResponse(
        transformation_id=transformation.id,
        status=transformation.status,
        outputs=[
            OutputPayload(format_type=OutputFormat(o.format_type), content=o.content, quality_score=o.quality_score)
            for o in outputs
        ],
    )


@router.get("/transform/{transformation_id}/outputs/{format_type}")
def get_single_output(transformation_id: int, format_type: OutputFormat, db: Session = Depends(get_db)) -> dict:
    output = db.scalar(
        select(Output).where(Output.transformation_id == transformation_id, Output.format_type == format_type.value)
    )
    if output is None:
        raise HTTPException(status_code=404, detail="Output not found")
    return output.content


@router.get("/history")
def history(db: Session = Depends(get_db)) -> dict:
    records = db.scalars(select(Transformation).order_by(Transformation.created_at.desc())).all()
    return {
        "items": [
            {
                "id": r.id,
                "input_type": r.input_type,
                "status": r.status,
                "created_at": r.created_at.isoformat(),
            }
            for r in records
        ]
    }


@router.post("/export/{transformation_id}")
def export(transformation_id: int, formats: list[OutputFormat], export_type: str, db: Session = Depends(get_db)) -> dict:
    _ = db.get(Transformation, transformation_id)
    if _ is None:
        raise HTTPException(status_code=404, detail="Transformation not found")
    return {
        "transformation_id": transformation_id,
        "export_type": export_type,
        "formats": [f.value for f in formats],
        "download_url": f"/downloads/{transformation_id}.{export_type}",
    }


@router.post("/publish/{output_id}")
def publish(output_id: int, platform: str, content: str, db: Session = Depends(get_db)) -> dict:
    output = db.get(Output, output_id)
    if output is None:
        raise HTTPException(status_code=404, detail="Output not found")
    return {"output_id": output_id, "platform": platform, "status": "queued", "preview": content[:140]}
