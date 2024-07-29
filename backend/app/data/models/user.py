from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    ForeignKey,
    String,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import Status


class User(RecordModel):
    __tablename__ = "users"
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
    # organization_id: Mapped[UUID | None] = mapped_column(
    #     Uuid,
    #     ForeignKey("organizations.id", ondelete="set null"),
    #     nullable=True,
    # )
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    phone_number: Mapped[str | None] = mapped_column(
        String(15), nullable=True, default=None
    )
    phone_number_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )
    profile_settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    # owner_id:
    # groups:
    # attributes:
    # roles:
    # scopes:
    last_login_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None,
    )
    accepted_terms_of_service: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    email_newsletters_and_changelogs: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    email_promotions_and_events: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| user_id           | Unique identifier for the user.                  |
| tenant_id         | ID of the associated tenant.                     |
| status            | Status of the user (e.g., active, inactive).     |
| username          | Username of the user.                            |
| first_name        | First name of the user.                          |
| last_name         | Last name of the user.                           |
| email             | Email address of the user.                       |
| phone_number      | Phone number of the user.                        |
| credentials       | Credentials of the user (e.g., password hash).   |
| owner_id          | ID of the user who owns this user (if applicable).|
| owned_groups      | List of groups owned by the user.                |
| owned_roles       | List of roles owned by the user.                 |
| owned_scopes      | List of scopes owned by the user.                |
| owned_attributes  | List of attributes owned by the user.            |
| last_login_at     | Timestamp of the user's last login.              |
| metadata          | JSON field for additional user metadata.         |
| description       | Description of the user.                         |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
