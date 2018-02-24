"""empty message

Revision ID: fb7fafec60f9
Revises: e26c6226843e
Create Date: 2018-02-24 10:51:45.049513

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = 'fb7fafec60f9'
down_revision = 'e26c6226843e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POLYGON'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('location', 'geometry')
    # ### end Alembic commands ###