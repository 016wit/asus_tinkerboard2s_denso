# app/job/views.py
from flask_restful import Resource, reqparse
from app.db import db
from app.models import ReportOr, ReportOrSchema, SBox
from datetime import datetime
from sqlalchemy import and_, extract
from flask_restful import inputs

parser = reqparse.RequestParser()
parser.add_argument("datetime_stamp", type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), required=True)
parser.add_argument('count_val', type=int, required=True)
parser.add_argument('pp_plan_val', type=int, required=True)
parser.add_argument('or_val', type=float, required=True)


class ReportOrListEndPoint(Resource):
    def get(self, *args, **kwargs):
        records = ReportOr.query.all()
        schema = ReportOrSchema(many=True)
        return schema.dump(records)


class ReportOrEndPoint(Resource):
    def post(self, serial):
        args = parser.parse_args()
        current_time = args["datetime_stamp"]
        record = SBox.query.filter(SBox.serialKey == serial).first()

        last = ReportOr.query.filter(ReportOr.vir_id == record.id,
                                     ReportOr.datetime_stamp.startswith(current_time.strftime("%Y-%m-%d")),
                                     current_time.hour == extract('hour', ReportOr.datetime_stamp)
                                     ).order_by(ReportOr.id.desc())

        schema = ReportOrSchema()

        if last.count():
            last[0].count_val = args["count_val"]
            last[0].pp_plan_val = args["pp_plan_val"]
            last[0].or_val = args["or_val"]
            db.session.commit()
            return schema.dump(last[0])
        else:
            record = ReportOr(
                vir_id=record.id,
                datetime_stamp=args["datetime_stamp"].replace(minute=0),
                count_val=args["count_val"],
                pp_plan_val=args["pp_plan_val"],
                or_val=args["or_val"]
            )
            db.session.add(record)
            db.session.commit()

        record = ReportOr.query.order_by(ReportOr.id.desc()).first()
        return schema.dump(record)
