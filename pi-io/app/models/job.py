from app import ma
from app.db import db
from datetime import datetime


class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    date_issue = db.Column(db.DATETIME, default=datetime.now())
    config_id = db.Column(db.Integer, db.ForeignKey('config.id'), nullable=False)
    work_result = db.relationship('WorkResult', backref='config', lazy=True)

    def __repr__(self):
        return '<Job: {}>'.format(self.date_issue)


class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Job
        # fields = "__all__"
