"""empty message

Revision ID: 231457bcc365
Revises: bee9ec0df149
Create Date: 2023-02-24 16:57:51.529140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '231457bcc365'
down_revision = 'bee9ec0df149'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.String(length=100), nullable=True),
    sa.Column('recepient_acc_id', sa.String(length=100), nullable=True),
    sa.Column('intent_id', sa.String(length=100), nullable=True),
    sa.Column('intent_secret', sa.String(length=100), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_info')
    # ### end Alembic commands ###