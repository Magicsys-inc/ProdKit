from typing import Any
from uuid import UUID

from citext import CIText
from sqlalchemy import Boolean, ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.core.exceptions import ProdkitError
from app.infra.kit.enums import Status


class NotKnownOrganizationError(ProdkitError):
    def __init__(self) -> None:
        super().__init__("This organization is not found.")


class Organization(RecordModel):
    __tablename__ = "organizations"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    account_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("accounts.id", ondelete="set null"),
        nullable=True,
    )
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    name: Mapped[str] = mapped_column(CIText(), nullable=False, unique=True)
    # owner_id:
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    phone_number: Mapped[str | None] = mapped_column(
        String(15), nullable=True, default=None
    )
    phone_number_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    avatar_url: Mapped[str] = mapped_column(String, nullable=False)
    profile_settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    feature_settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    # industry:
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| organization_id   | Unique identifier for the organization.          |
| tenant_id         | ID of the associated tenant.                     |
| status            | Status of the organization (e.g., active, inactive).|
| name              | Name of the organization.                        |
| email             | Contact email of the organization.               |
| phone_number      | Contact phone number of the organization.        |
| metadata          | JSON field for additional organization metadata. |
| description       | Description of the organization.                 |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
