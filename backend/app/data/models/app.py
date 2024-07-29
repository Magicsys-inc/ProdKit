from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import Status


class App(RecordModel):
    __tablename__ = "apps"
    __table_args__ = ()

    schema: str = ""

    name: Mapped[str | None] = mapped_column(String(30), nullable=True, default=None)
    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
