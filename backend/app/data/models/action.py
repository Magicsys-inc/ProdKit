from uuid import UUID

from citext import CIText
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import Status


class Action(RecordModel):
    __tablename__ = "actions"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    name: Mapped[str] = mapped_column(CIText(), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute        | Description                                                      |
|------------------|------------------------------------------------------------------|
| action_id        | Unique identifier for the action.                                |
| name             | Name of the action (e.g., 'login', 'file_upload').               |
| description      | Description of the action and its purpose.                       |
| created_at       | Timestamp when the attribute was created.                        |
| updated_at       | Timestamp when the attribute was last updated.                   |
| deleted_at       | Timestamp when the attribute was deleted.                        |
"""
