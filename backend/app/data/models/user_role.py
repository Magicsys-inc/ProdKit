from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import TimestampedModel


class UserRole(TimestampedModel):
    __tablename__ = "user_roles"
    __table_args__ = ()

    schema: str = ""

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="set null"),
        nullable=True,
    )
    role_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("roles.id", ondelete="set null"),
        nullable=True,
    )


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| user_role_id      | Unique identifier for the user-role link.        |
| user_id           | ID of the user.                                  |
| role_id           | ID of the role.                                  |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
