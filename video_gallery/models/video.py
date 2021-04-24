from sqlalchemy import desc

from ..db import db


class Video(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    thumbnail_url = db.Column(db.String(2048), nullable=False)
    published_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)

    @staticmethod
    def latest() -> 'Video':
        return Video.query.order_by(desc(Video.published_at)).limit(1).first()
