from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import TimestampedModel


class UserGroup(TimestampedModel):
    __tablename__ = "user_groups"
    __table_args__ = ()

    schema: str = ""

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="set null"),
        nullable=True,
    )
    group_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("groups.id", ondelete="set null"),
        nullable=True,
    )


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| user_group_id     | Unique identifier for the user-group link.       |
| user_id           | ID of the user.                                  |
| group_id          | ID of the group.                                 |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
