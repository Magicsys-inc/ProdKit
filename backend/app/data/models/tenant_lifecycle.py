from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import Status


class TenantLifecycle(RecordModel):
    __tablename__ = "tenant_lifecycles"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    event: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    event_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None,
    )
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)


"""
| Attribute           | Description                                                      |
|---------------------|------------------------------------------------------------------|
| tenant_lifecycle_id | Unique identifier for the tenant-lifecycle link.                 |
| tenant_id           | ID of the associated tenant.                                     |
| phase               | The current phase or stage of the tenant's lifecycle (e.g., onboarded, provisioned).|
| phase_at            | Timestamp indicating when the tenant entered the current phase.  |
| details             | JSON field for additional details or context about the lifecycle.|
| created_at          | Timestamp when the attribute was created.                        |
| updated_at          | Timestamp when the attribute was last updated.                   |
| deleted_at          | Timestamp when the attribute was deleted.                        |
"""
