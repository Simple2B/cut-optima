"""user calculation_enabled

Revision ID: ec58c3ac5211
Revises: 26ea19152d95
Create Date: 2023-11-03 13:06:10.868668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec58c3ac5211'
down_revision = '26ea19152d95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('calculation_enabled', sa.Boolean(), default=True, server_default='true'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'calculation_enabled')
    # ### end Alembic commands ###
