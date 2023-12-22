"""Add geom field for RestaurantModel to store and handle spatial data

Revision ID: 0e919c5596b2
Revises: 6daef9acb1b9
Create Date: 2023-12-18 18:26:48.976899

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry


# revision identifiers, used by Alembic.
revision = '0e919c5596b2'
down_revision = '6daef9acb1b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('restaurant', sa.Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=False))


def downgrade():
    op.drop_column('restaurant', 'geom')
