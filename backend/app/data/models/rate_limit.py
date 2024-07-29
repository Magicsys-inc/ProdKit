from uuid import UUID

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import RecordModel


class RateLimit(RecordModel):
    __tablename__ = "rate_limits"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    # endpoint:
    # limit:
    # period:
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )
