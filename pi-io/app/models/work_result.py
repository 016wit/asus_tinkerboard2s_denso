from app import ma
from app.db import db
from datetime import datetime


class WorkResult(db.Model):
    __tablename__ = 'work_result'

    id = db.Column(db.Integer, primary_key=True)
    date_issue = db.Column(db.DATETIME, default=datetime.now())
    result = db.Column(db.FLOAT, default=0)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    def __repr__(self):
        return '<WorkResult: {}>'.format(self.date_issue)


class WorkResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkResult
        # fields = "__all__"
