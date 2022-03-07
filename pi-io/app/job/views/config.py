# app/job/views.py
from flask_restful import Resource, reqparse
from app import db
from app.models import Config, ConfigSchema

# from flask import request
# from . import job
parser = reqparse.RequestParser()
parser.add_argument('profile', type=str, required=True)
parser.add_argument('description', type=str, required=True)
parser.add_argument('target', type=int, required=True)
parser.add_argument('tt', type=int, required=True)
parser.add_argument('station', type=str, required=True)
parser.add_argument('threshold', type=int, required=True)


class ConfigListEndPoint(Resource):
    def get(self):
        records = Config.query.all()
        config_schema = ConfigSchema(many=True)
        return config_schema.dump(records)

    def post(self):
        args = parser.parse_args()
        record = Config(
            profile=args["profile"],
            description=args["description"],
            target=args["target"],
            tt=args["tt"],
            station=args["station"],
            threshold=args["threshold"],
        )
        db.session.add(record)
        db.session.commit()
        records = Config.query.order_by(Config.id.desc()).first()
        config_schema = ConfigSchema()
        return config_schema.dump(records)
