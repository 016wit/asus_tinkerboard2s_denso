# app/job/views.py
from flask_restful import Resource, reqparse
from app import db
from app.models import SBox, SBoxSchema
from datetime import datetime

# from flask import request
# from . import job
parser = reqparse.RequestParser()
parser.add_argument('key', type=int, required=True)


class SBoxEndPointList(Resource):
    def get(self, *args, **kwargs):
        records = SBox.query.all()
        jobs_schema = SBoxSchema(many=True)
        return jobs_schema.dump(records)


class SBoxEndPoint(Resource):
    def get(self, serial):
        records = SBox.query.filter(SBox.serialKey.contains(serial))
        schema = SBoxSchema(many=True)
        return schema.dump(records)
