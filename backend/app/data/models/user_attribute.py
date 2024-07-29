from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import TimestampedModel


class UserAttribute(TimestampedModel):
    __tablename__ = "user_attributes"
    __table_args__ = ()

    schema: str = ""

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="set null"),
        nullable=True,
    )
    attribute_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("attributes.id", ondelete="set null"),
        nullable=True,
    )


"""
| Attribute         | Description                                      |
|-------------------|--------------------------------------------------|
| user_attribute_id | Unique identifier for the user-attribute link.   |
| user_id           | ID of the user.                                  |
| attribute_id      | ID of the attribute.                             |
| created_at        | Timestamp when the attribute was created.        |
| updated_at        | Timestamp when the attribute was last updated.   |
| deleted_at        | Timestamp when the attribute was deleted.        |
"""
