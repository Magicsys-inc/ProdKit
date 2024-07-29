from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import AccountLevel, Status


class Account(RecordModel):
    __tablename__ = "accounts"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    # TODO: Correct it based on account_type table
    account_type: Mapped[AccountLevel] = mapped_column(
        StringEnum(AccountLevel), nullable=False, default=AccountLevel.DEFAULT
    )
    # organization_id: Mapped[UUID | None] = mapped_column(
    #     Uuid,
    #     ForeignKey("organizations.id", ondelete="set null"),
    #     nullable=True,
    # )
    # user_id: Mapped[UUID | None] = mapped_column(
    #     Uuid,
    #     ForeignKey("users.id", ondelete="set null"),
    #     nullable=True,
    # )
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    username: Mapped[str | None] = mapped_column(
        String(30), nullable=True, default=None
    )
    email: Mapped[str | None] = mapped_column(String(254), nullable=True, default=None)
    phone_number: Mapped[str | None] = mapped_column(
        String(15), nullable=True, default=None
    )
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    currency: Mapped[str | None] = mapped_column(String(3))
    # credentials:
    avatar_url: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )
    bio: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    preferences: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    is_details_submitted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    # roles

    # Anonymous
    # Credintials
    # Posthog


"""
| Attribute            | Description                                      |
|----------------------|--------------------------------------------------|
| account_id           | Unique identifier for the account.               |
| tenant_id            | ID of the associated tenant.                     |
| organization_id      | ID of the associated organization.               |
| status               | Status of the account (e.g., active, inactive).  |
| username             | Username for the account login.                  |
| email                | Email address of the user.                       |
| phone_number         | Phone number of the user.                        |
| is_details_submitted | Boolean for the account details submittion.      |
| profile_picture      | URL to the user's profile picture.               |
| bio                  | Short biography or description of the user.      |
| settings             | JSON field for user-specific settings.           |
| preferences          | JSON field for user preferences.                 |
| metadata             | JSON field for additional account metadata.      |
| created_at           | Timestamp when the attribute was created.        |
| updated_at           | Timestamp when the attribute was last updated.   |
| deleted_at           | Timestamp when the attribute was deleted.        |
"""
