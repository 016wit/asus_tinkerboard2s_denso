# app/job/views.py
from flask_restful import Resource, reqparse
from app.db import db
from app.models import ReportOrAnalysis, ReportOrAnalysisSchema, SBox
from datetime import datetime
from sqlalchemy import and_, extract

parser = reqparse.RequestParser()
parser.add_argument("datetime_stamp", type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'), required=True)
parser.add_argument('lost_val', type=int, required=True)
parser.add_argument('meeting_val', type=int, required=True)
parser.add_argument('run_val', type=int, required=True)
parser.add_argument('down_val', type=int, required=True)
parser.add_argument('short_breakdown_val', type=int, required=True)


class ReportOrAnalysisListEndPoint(Resource):
    def get(self, *args, **kwargs):
        records = ReportOrAnalysis.query.all()
        schema = ReportOrAnalysisSchema(many=True)
        return schema.dump(records)


class ReportOrAnalysisEndPoint(Resource):
    def post(self, serial):
        args = parser.parse_args()
        current_time = args["datetime_stamp"]
        record = SBox.query.filter(SBox.serialKey == serial).first()

        last = ReportOrAnalysis.query.filter(ReportOrAnalysis.vir_id == record.id,
                                             ReportOrAnalysis.datetime_stamp.startswith(
                                                 current_time.strftime("%Y-%m-%d")),
                                             current_time.hour == extract('hour',
                                                                          ReportOrAnalysis.datetime_stamp)
                                             ).order_by(ReportOrAnalysis.id.desc())

        schema = ReportOrAnalysisSchema()

        if last.count():
            last[0].lost_val = args["lost_val"]
            last[0].meeting_val = args["meeting_val"]
            last[0].run_val = args["run_val"]
            last[0].down_val = args["down_val"]
            last[0].short_breakdown_val = args["short_breakdown_val"]
            db.session.commit()
            return schema.dump(last[0])
        else:
            record = ReportOrAnalysis(
                vir_id=record.id,
                datetime_stamp=args["datetime_stamp"].replace(minute=0),
                lost_val=args["lost_val"],
                meeting_val=args["meeting_val"],
                run_val=args["run_val"],
                down_val=args["down_val"],
                short_breakdown_val=args["short_breakdown_val"]
            )
            db.session.add(record)
            db.session.commit()

        record = ReportOrAnalysis.query.order_by(ReportOrAnalysis.id.desc()).first()
        return schema.dump(record)
