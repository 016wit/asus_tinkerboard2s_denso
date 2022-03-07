from app import ma
from app.db import db
from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Enum, Float, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TEXT, TINYINT


class SBox(db.Model):
    __tablename__ = '108_sbox'

    id = Column(INTEGER(11), primary_key=True)
    masterKey = Column(String(17))
    serialKey = Column(String(20))
    sboxtypeID = Column(INTEGER(11))
    aliasName = Column(String(50))
    userID = Column(INTEGER(11))
    machineID = Column(INTEGER(11))
    factoryType = Column(INTEGER(11))
    sboxReady = Column(Enum('Y', 'N'), server_default=text("'N'"))
    datetimeCreate = Column(TIMESTAMP, nullable=False,
                            server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class SBoxSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SBox
        # fields = "__all__"
