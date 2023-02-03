"""empty message

Revision ID: 1b0918292029
Revises: 616a6174d218
Create Date: 2023-02-03 16:42:47.277627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b0918292029'
down_revision = '616a6174d218'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('review', sa.Text(), nullable=True),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('property', sa.Column('average_rating', sa.String(length=10), nullable=True))
    op.add_column('property', sa.Column('created_at', sa.Date(), nullable=True))
    op.add_column('property', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('property_image', sa.Column('created_at', sa.Date(), nullable=True))
    op.add_column('property_image', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property_image', 'updated_at')
    op.drop_column('property_image', 'created_at')
    op.drop_column('property', 'updated_at')
    op.drop_column('property', 'created_at')
    op.drop_column('property', 'average_rating')
    op.drop_table('review')
    # ### end Alembic commands ###