"""empty message

Revision ID: c4752efa2b5f
Revises: d709cf1944b9
Create Date: 2023-02-08 18:26:00.422841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4752efa2b5f'
down_revision = 'd709cf1944b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('address', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property', 'address')
    # ### end Alembic commands ###