from app import ma
from app.db import db
from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Enum, Float, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TEXT, TINYINT, FLOAT


class ReportOr(db.Model):
    __tablename__ = '108_report_or'

    id = Column(INTEGER(11), primary_key=True)
    vir_id = Column(INTEGER(11), nullable=False, index=True)
    datetime_stamp = Column(TIMESTAMP, nullable=False,
                            server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    count_val = Column(INTEGER(11), nullable=False, index=True)
    pp_plan_val = Column(INTEGER(11), nullable=False, index=True)
    or_val = Column(FLOAT, nullable=False, index=True)


class ReportOrSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReportOr
        # fields = "__all__"
