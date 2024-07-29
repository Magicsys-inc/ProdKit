from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.models import RecordModel


class TenantActivity(RecordModel):
    __tablename__ = "tenant_activities"
    __table_args__ = ()

    schema: str = ""

    tenant_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("tenants.id", ondelete="set null"),
        nullable=True,
    )
    action_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("actions.id", ondelete="set null"),
        nullable=True,
    )
    # object_type: # TODO: Resource type?
    # object_id:
    # subject_type: TODO: From Sub?
    # subject_id:
    # ip_address:
    # user_agent:
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute        | Description                                                        |
|------------------|--------------------------------------------------------------------|
| tenant_activity_id | Unique identifier for the tenant-activity link.                  |
| tenant_id        | ID of the associated tenant.                                       |
| action_id        | ID of Action performed by the user (e.g., 'login', 'file_upload'). |
| object_type      | Type of object involved in the action (e.g., 'File', 'Document').  |
| object_id        | ID of the object involved in the action.                           |
| subject_type     | Type of the subject of the action (e.g., 'User', 'Organization').  |
| subject_id       | ID of the subject of the action.                                   |
| ip_address       | IP address of the user.                                            |
| user_agent       | User agent of the browser or client.                               |
| data             | Additional data related to the action (e.g., JSON field).          |
| description      | Description of the activity for context.                           |
| created_at       | Timestamp when the attribute was created.                          |
| updated_at       | Timestamp when the attribute was last updated.                     |
| deleted_at       | Timestamp when the attribute was deleted.                          |
"""
