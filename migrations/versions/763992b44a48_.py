"""empty message

Revision ID: 763992b44a48
Revises: 0f8bc241d454
Create Date: 2023-02-02 19:29:15.141335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '763992b44a48'
down_revision = '0f8bc241d454'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('city', sa.String(length=200), nullable=True),
    sa.Column('state', sa.String(length=200), nullable=True),
    sa.Column('zipcode', sa.String(length=10), nullable=True),
    sa.Column('guest_space', sa.String(length=10), nullable=True),
    sa.Column('beds', sa.String(length=10), nullable=True),
    sa.Column('bedrooms', sa.String(length=10), nullable=True),
    sa.Column('about_property', sa.Text(), nullable=True),
    sa.Column('amenities', sa.String(length=200), nullable=True),
    sa.Column('house_rules', sa.String(length=200), nullable=True),
    sa.Column('price_per_night', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property_image',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('picture_name', sa.String(length=200), nullable=True),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property_image')
    op.drop_table('property')
    # ### end Alembic commands ###