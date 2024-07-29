from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import TenantLevel


class TenantType(RecordModel):
    __tablename__ = "tenant_types"
    __table_args__ = ()

    schema: str = ""

    name: Mapped[TenantLevel] = mapped_column(
        StringEnum(TenantLevel), nullable=False, default=TenantLevel.DEFAULT
    )
    # permissions:
    # features:
    # limitations: # like max_sessions, max_users, max_storage, max_bandwidth
    # price:
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )
