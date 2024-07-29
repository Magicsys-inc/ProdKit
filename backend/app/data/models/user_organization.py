from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from app.data.dbs.postgres.models import TimestampedModel

from .organization import Organization
from .user import User


class UserOrganization(TimestampedModel):
    __tablename__ = "users_organizations"
    __table_args__ = ()

    schema: str = ""

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
        primary_key=True,
    )

    organization_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    @declared_attr
    def user(self) -> "Mapped[User]":
        return relationship("User", lazy="raise")

    @declared_attr
    def organization(self) -> "Mapped[Organization]":
        return relationship("Organization", lazy="raise")

    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| user_org_id       | Unique identifier for the user-organization link.|
| user_id           | ID of the user.                                  |
| organization_id   | ID of the organization.                          |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
