"""empty message

Revision ID: bee9ec0df149
Revises: 314714ea816a
Create Date: 2023-02-24 16:46:50.421739

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bee9ec0df149'
down_revision = '314714ea816a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image_name', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('account_verified', sa.Boolean(), nullable=True))
    op.drop_column('user', 'photo_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('photo_name', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('user', 'account_verified')
    op.drop_column('user', 'image_name')
    # ### end Alembic commands ###
