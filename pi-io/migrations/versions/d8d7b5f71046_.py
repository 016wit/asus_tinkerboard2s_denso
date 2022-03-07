"""empty message

Revision ID: d8d7b5f71046
Revises: 
Create Date: 2021-01-14 16:40:42.194154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8d7b5f71046'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('target', sa.Integer(), nullable=True),
    sa.Column('tt', sa.Integer(), nullable=True),
    sa.Column('station', sa.String(length=64), nullable=True),
    sa.Column('threshold', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('config')
    # ### end Alembic commands ###