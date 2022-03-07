from app import ma
from app.db import db
from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Enum, Float, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TEXT, TINYINT


class ReportStatus(db.Model):
    __tablename__ = '108_report_status'

    id = Column(INTEGER(11), primary_key=True)
    sboxName = Column(String(21), nullable=False, index=True)
    statusValue = Column(INTEGER(2), nullable=False)
    userID = Column(INTEGER(11), nullable=False, index=True)
    datetimeStamp = Column(String(15), nullable=False, index=True)
    timeStampLocal = Column(DateTime, nullable=False)
    dateStamp = Column(Date, nullable=False, index=True)
    timeStamp = Column(TIMESTAMP, nullable=False,
                       server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class ReportStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReportStatus
        # fields = "__all__"
