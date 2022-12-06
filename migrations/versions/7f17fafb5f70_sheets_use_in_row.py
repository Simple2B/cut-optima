"""empty message

Revision ID: 7f17fafb5f70
Revises: bf87a25d315f
Create Date: 2022-12-06 10:32:23.209025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7f17fafb5f70"
down_revision = "bf87a25d315f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sheets",
        sa.Column("use_in_row", sa.Boolean(), nullable=True, server_default="f"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sheets", "use_in_row")
    # ### end Alembic commands ###
