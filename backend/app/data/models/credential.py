from typing import Any
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import CredentialType


class Credential(RecordModel):
    __tablename__ = "credentials"
    __table_args__ = (
        UniqueConstraint("user_id", "type", name="unique_user_credential_type"),
    )

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="set null"),
        nullable=True,
    )
    type: Mapped[CredentialType] = mapped_column(
        StringEnum(CredentialType), nullable=False, default=CredentialType.PASSWORD
    )
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)


"""
| Attribute        | Description                                     |
|------------------|-------------------------------------------------|
| credential_id    | Unique identifier for the credential.           |
| user_id          | ID of the associated user.                      |
| type             | Type of credential (e.g., password, token).     |
| value            | Value of the credential (e.g., hashed password).|
| created_at       | Timestamp when the attribute was created.       |
| updated_at       | Timestamp when the attribute was last updated.  |
| deleted_at       | Timestamp when the attribute was deleted.       |
"""
