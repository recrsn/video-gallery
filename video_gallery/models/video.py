from sqlalchemy import desc, Index

from video_gallery.models.types.ts_vector import TSVector
from ..db import db


class Video(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    thumbnail_url = db.Column(db.String(2048), nullable=False)
    published_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)

    __ts_vector__ = db.Column(TSVector(),
                              db.Computed("to_tsvector('english', title || ' ' || description)",
                                          persisted=True))

    __table_args__ = (
        Index('ix_video___ts_vector__', __ts_vector__, postgresql_using='gin'),
    )

    @staticmethod
    def latest() -> 'Video':
        return Video.query.order_by(desc(Video.published_at)).limit(1).first()
