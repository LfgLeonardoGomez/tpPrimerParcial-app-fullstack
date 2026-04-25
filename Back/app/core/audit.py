from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class AuditMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )