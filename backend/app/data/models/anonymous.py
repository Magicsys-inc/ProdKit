from app.data.dbs.postgres.models import RecordModel


class Anonymous(RecordModel):
    __tablename__ = "anonymouses"
    __table_args__ = ()

    schema: str = ""
