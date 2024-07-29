from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import TimestampedModel


class UserResource(TimestampedModel):
    __tablename__ = "user_resources"
    __table_args__ = ()

    schema: str = ""

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="set null"),
        nullable=True,
    )
    resource_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("resources.id", ondelete="set null"),
        nullable=True,
    )
    # permission:


"""
| Attribute        | Description                                                             |
|------------------|-------------------------------------------------------------------------|
| user_resource_id | Unique identifier for the user-resource link.                           |
| user_id          | ID of the user associated with the resource.                            |
| resource_id      | ID of the resource.                                                     |
| permission       | Permission level the user has on the resource (e.g., read, write, admin).|
| created_at       | Timestamp when the attribute was created.                               |
| updated_at       | Timestamp when the attribute was last updated.                          |
| deleted_at       | Timestamp when the attribute was deleted.                               |
"""
