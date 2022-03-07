# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
# local imports
# from config import app_config
from flask_cors import CORS

# db variable initialization
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name="production"):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_pyfile('config.py')
    # Initialize SQL-Alchemy
    from app.db import db
    db.init_app(app)
    # Initialize Marshmallow
    ma.init_app(app)
    # Initialize Migration
    # migrate.init_app(app, db)
    # Initialize API
    api = Api(app)

    from app import models
    from app.job.views import ConfigListEndPoint, JobListEndPoint, WorkResultListEndPoint, WorkResultEndPoint
    from app.sbox.views import SBoxEndPointList, SBoxEndPoint
    from app.result.views import ReportOrListEndPoint, ReportOrEndPoint
    from app.result.views import ReportOrAnalysisListEndPoint, ReportOrAnalysisEndPoint

    api.add_resource(ConfigListEndPoint, '/jobs')
    api.add_resource(JobListEndPoint, '/work')
    api.add_resource(WorkResultListEndPoint, '/result')
    api.add_resource(SBoxEndPointList, '/sbox')
    api.add_resource(SBoxEndPoint, '/sbox/<serial>')
    api.add_resource(ReportOrListEndPoint, '/or_result')
    api.add_resource(ReportOrEndPoint, '/or_result/<serial>')
    api.add_resource(ReportOrAnalysisListEndPoint, '/or_analysis')
    api.add_resource(ReportOrAnalysisEndPoint, '/or_analysis/<serial>')

    # temporary route
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app
