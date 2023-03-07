"""empty message

Revision ID: 95c44edb91ea
Revises: e1c03fec8591
Create Date: 2023-02-24 19:03:19.176392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95c44edb91ea'
down_revision = 'e1c03fec8591'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment_info', sa.Column('customer', sa.String(length=100), nullable=True))
    op.add_column('payment_info', sa.Column('recipient', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment_info', 'recipient')
    op.drop_column('payment_info', 'customer')
    # ### end Alembic commands ###