from typing import Any
from uuid import UUID

from citext import CIText
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import Status


class Scope(RecordModel):
    __tablename__ = "scopes"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    name: Mapped[str] = mapped_column(CIText(), nullable=False, unique=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| scope_id          | Unique identifier for the scope.                 |
| tenant_id         | ID of the associated tenant.                     |
| status            | Status of the scope (e.g., active, inactive).    |
| name              | Name of the scope.                               |
| owner_id          | ID of the user who owns the scope.               |
| metadata          | JSON field for additional scope metadata.        |
| description       | Description of the scope.                        |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
