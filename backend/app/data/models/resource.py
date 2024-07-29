from typing import Any
from uuid import UUID

from citext import CIText
from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import ResourceType, Status


class Resource(RecordModel):
    __tablename__ = "resources"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    organization_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("organizations.id", ondelete="set null"),
        nullable=True,
    )
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    name: Mapped[str] = mapped_column(CIText(), nullable=False, unique=True)
    # TODO: Change it in the near future with resource_type table
    type: Mapped[ResourceType] = mapped_column(
        StringEnum(ResourceType), nullable=False, default=ResourceType.OTHER
    )
    # owner_id:
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False)
    tags: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    location: Mapped[str | None] = mapped_column(
        String(254), nullable=True, default=None
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute        | Description                                                             |
|------------------|-------------------------------------------------------------------------|
| resource_id      | Unique identifier for the resource.                                     |
| tenant_id        | ID of the associated tenant.                                            |
| organization_id  | ID of the associated organization.                                      |
| status           | Status of the resource (e.g., active, inactive).                        |
| name             | Name of the resource.                                                   |
| type             | Type of the resource (e.g., files, documents, settings).                |
| owner_id         | ID of the user who owns the resource.                                   |
| is_public        | Boolean indicating if the resource is public.                           |
| tags             | Tags associated with the resource for categorization and searchability. |
| location         | Physical or virtual location of the resource (e.g., URL, file path).    |
| metadata         | JSON field for additional resource metadata.                            |
| description      | Description of the resource.                                            |
| created_at       | Timestamp when the attribute was created.                               |
| updated_at       | Timestamp when the attribute was last updated.                          |
| deleted_at       | Timestamp when the attribute was deleted.                               |
"""
