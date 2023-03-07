"""empty message

Revision ID: 3fbcd6ef0e31
Revises: 7c667be9e106
Create Date: 2023-02-22 17:51:40.039985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fbcd6ef0e31'
down_revision = '7c667be9e106'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('type_of_place', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property', 'type_of_place')
    # ### end Alembic commands ###