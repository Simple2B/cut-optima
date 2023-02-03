"""contact us

Revision ID: 59534c255589
Revises: 71d3cb2dbedc
Create Date: 2023-02-01 12:21:45.962555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59534c255589"
down_revision = "71d3cb2dbedc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("contact_name", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "users", sa.Column("contact_email", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "users", sa.Column("contact_phone", sa.String(length=64), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "contact_phone")
    op.drop_column("users", "contact_email")
    op.drop_column("users", "contact_name")
    # ### end Alembic commands ###