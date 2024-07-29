from typing import Any
from uuid import UUID

from citext import CIText
from sqlalchemy import (
    ForeignKey,
    String,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import RecordModel


class TenantSetting(RecordModel):
    __tablename__ = "tenant_settings"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(CIText(), nullable=False, unique=True)
    value: Mapped[str] = mapped_column(String(50), nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute     | Description                                                      |
|---------------|------------------------------------------------------------------|
| tenant_set_id | Unique identifier for the tenant-settings link.                  |
| tenant_id     | ID of the associated tenant.                                     |
| name          | Name of the setting (e.g., 'max_users').                         |
| value         | Value of the setting (e.g., '100').                              |
| description   | Description of the setting and its purpose.                      |
| created_at    | Timestamp when the attribute was created.                        |
| updated_at    | Timestamp when the attribute was last updated.                   |
| deleted_at    | Timestamp when the attribute was deleted.                        |
"""
