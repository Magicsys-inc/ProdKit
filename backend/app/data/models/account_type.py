from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import AccountLevel


class AccountType(RecordModel):
    __tablename__ = "account_types"
    __table_args__ = ()

    schema: str = ""

    name: Mapped[AccountLevel] = mapped_column(
        StringEnum(AccountLevel), nullable=False, default=AccountLevel.DEFAULT
    )
    # permissions:
    # features:
    # limitations: # like max_sessions
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )
