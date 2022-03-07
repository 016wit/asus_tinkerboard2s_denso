# app/job/views.py
from flask_restful import Resource, reqparse
from app import db
from app.models import WorkResult, WorkResultSchema
from datetime import datetime

# from flask import request
# from . import job
parser = reqparse.RequestParser()
parser.add_argument('job_id', type=int, required=True)
parser.add_argument('result', type=float, required=True)


class WorkResultListEndPoint(Resource):
    def get(self):
        records = WorkResult.query.all()
        jobs_schema = WorkResultSchema(many=True)
        return jobs_schema.dump(records)

    def post(self):
        args = parser.parse_args()
        record = WorkResult(
            job_id=args["job_id"],
            result=args["result"],
            date_issue=datetime.now(),
        )
        db.session.add(record)
        db.session.commit()
        records = WorkResult.query.order_by(WorkResult.id.desc()).first()
        job_schema = WorkResultSchema()
        return job_schema.dump(records)


class WorkResultEndPoint(Resource):
    def post(self, record_id):
        current_time = datetime.now()
        args = parser.parse_args()
        records = WorkResult.query.order_by(WorkResult.date_issue.desc()).first()

        start = current_time.replace(minute=0)
        end = current_time.replace(minute=30)
        if start < records.date_issue < end:
            WorkResult.query.filter_by(id=record_id).update({
                "result": args["result"]
            })
        else:
            if current_time.minute < 30:
                stamp_time = current_time.replace(minute=0)
            else:
                stamp_time = current_time.replace(minute=30)

            record = WorkResult(
                job_id=args["job_id"],
                result=args["result"],
                date_issue=stamp_time,
            )
            db.session.add(record)
            db.session.commit()
        records = WorkResult.query.order_by(WorkResult.date_issue.desc()).first()
        work_result_schema = WorkResultSchema()
        return work_result_schema.dump(records)
