"""empty message

Revision ID: 23c1b65b0e13
Revises:
Create Date: 2021-04-24 18:50:15.132879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23c1b65b0e13'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('thumbnail_url', sa.String(length=2048), nullable=False),
    sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_video_published_at'), 'video', ['published_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_video_published_at'), table_name='video')
    op.drop_table('video')
    # ### end Alembic commands ###
