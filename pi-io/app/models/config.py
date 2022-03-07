from app import ma
from app.db import db


class Config(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.String(64))
    description = db.Column(db.String(200))
    target = db.Column(db.Integer)
    tt = db.Column(db.Integer)
    station = db.Column(db.String(64))
    threshold = db.Column(db.Integer)
    jobs = db.relationship('Job', backref='config', lazy=True)

    def __repr__(self):
        return '<Config: {}>'.format(self.profile)


class ConfigSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Config
        # sqla_session = db.session
        # fields = "__all__"
