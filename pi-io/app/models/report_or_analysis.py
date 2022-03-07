from app import ma
from app.db import db
from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Enum, Float, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TEXT, TINYINT, FLOAT


class ReportOrAnalysis(db.Model):
    __tablename__ = '108_report_or_analysis'

    id = Column(INTEGER(11), primary_key=True)
    vir_id = Column(INTEGER(11), nullable=False, index=True)
    datetime_stamp = Column(TIMESTAMP, nullable=False,
                            server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    lost_val = Column(INTEGER(11), nullable=False, index=True)
    meeting_val = Column(INTEGER(11), nullable=False, index=True)
    run_val = Column(INTEGER(11), nullable=False, index=True)
    down_val = Column(INTEGER(11), nullable=False, index=True)
    short_breakdown_val = Column(INTEGER(11), nullable=False, index=True)


class ReportOrAnalysisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReportOrAnalysis
        # fields = "__all__"
