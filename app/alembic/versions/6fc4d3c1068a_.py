"""empty message

Revision ID: 6fc4d3c1068a
Revises: dec15835dd01
Create Date: 2023-07-19 11:34:21.335226

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6fc4d3c1068a'
down_revision = 'dec15835dd01'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    op.drop_table('user_details')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_details',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('unique_id', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('password', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('otp', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_details_pkey')
    )
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('unique_id', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('filename', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('create_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='images_pkey')
    )
    # ### end Alembic commands ###
