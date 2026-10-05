from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class InputType(str, Enum):
    text = "text"
    pdf = "pdf"
    image = "image"
    video = "video"
    url = "url"


class OutputFormat(str, Enum):
    linkedin = "linkedin"
    twitter = "twitter"
    executive_summary = "executive_summary"
    video_script = "video_script"


class TransformParameters(BaseModel):
    tone: str = "Professional"
    audience: str = "General Public"
    length: str = "Medium"
    style: str = "Formal"
    language: str = "English"
    detail_level: str = "Overview"
    quality_cost_balance: float = Field(0.7, ge=0, le=1)


class TransformRequest(BaseModel):
    content: str
    input_type: InputType
    output_formats: list[OutputFormat]
    parameters: TransformParameters


class OutputPayload(BaseModel):
    format_type: OutputFormat
    content: dict
    quality_score: float


class TransformResponse(BaseModel):
    transformation_id: int
    status: str
    outputs: list[OutputPayload]


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    subscription_tier: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
