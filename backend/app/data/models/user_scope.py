from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import TimestampedModel


class UserScope(TimestampedModel):
    __tablename__ = "user_scopes"
    __table_args__ = ()

    schema: str = ""

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="set null"),
        nullable=True,
    )
    scope_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("scopes.id", ondelete="set null"),
        nullable=True,
    )


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| user_scope_id     | Unique identifier for the user-scope link.       |
| user_id           | ID of the user.                                  |
| scope_id          | ID of the scope.                                 |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
