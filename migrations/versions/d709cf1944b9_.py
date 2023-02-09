"""empty message

Revision ID: d709cf1944b9
Revises: 8f307a451fcf
Create Date: 2023-02-08 18:23:24.685744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd709cf1944b9'
down_revision = '8f307a451fcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('latitude', sa.String(length=200), nullable=True))
    op.add_column('property', sa.Column('longitude', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property', 'longitude')
    op.drop_column('property', 'latitude')
    # ### end Alembic commands ###
