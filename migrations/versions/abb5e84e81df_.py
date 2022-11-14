"""empty message

Revision ID: abb5e84e81df
Revises: 7e5ed84e72c5
Create Date: 2022-11-14 12:04:57.706832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abb5e84e81df'
down_revision = '7e5ed84e72c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('reset_password_uid', sa.String(length=64), nullable=True))
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_constraint('users_confirmation_token_key', 'users', type_='unique')
    op.drop_column('users', 'confirmation_token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmation_token', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.create_unique_constraint('users_confirmation_token_key', 'users', ['confirmation_token'])
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_column('users', 'reset_password_uid')
    op.drop_column('users', 'deleted')
    # ### end Alembic commands ###
