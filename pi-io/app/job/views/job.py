# app/job/views.py
from flask_restful import Resource, reqparse
from app import db
from app.models import Job, JobSchema
from datetime import datetime

# from flask import request
# from . import job
parser = reqparse.RequestParser()
parser.add_argument('config_id', type=int, required=True)


class JobListEndPoint(Resource):
    def get(self):
        records = Job.query.all()
        jobs_schema = JobSchema(many=True)
        return jobs_schema.dump(records)

    def post(self):
        args = parser.parse_args()
        record = Job(
            config_id=args["config_id"],
            date_issue=datetime.now(),
        )
        db.session.add(record)
        db.session.commit()
        records = Job.query.order_by(Job.id.desc()).first()
        job_schema = JobSchema()
        return job_schema.dump(records)
