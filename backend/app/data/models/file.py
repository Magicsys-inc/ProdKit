from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import Status


class File(RecordModel):
    __tablename__ = "files"
    __table_args__ = ()

    schema: str = ""

    # resource_id:
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    name: Mapped[str | None] = mapped_column(String(30), nullable=True, default=None)
    # file_path:
    # size:


"""
| Attribute   | Description                                                       |
|-------------|-------------------------------------------------------------------|
| file_id     | Unique identifier for the file.                                   |
| resource_id | ID of the associated resource.                                    |
| status      | Status of the file (e.g., active, archived).                      |
| name        | Name of the file.                                                 |
| file_path   | Path to the file in the filesystem or storage service.            |
| size        | Size of the file in bytes.                                        |
| created_at  | Timestamp when the attribute was created.                         |
| updated_at  | Timestamp when the attribute was last updated.                    |
| deleted_at  | Timestamp when the attribute was deleted.                         |
"""
