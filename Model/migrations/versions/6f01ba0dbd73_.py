"""empty message

Revision ID: 6f01ba0dbd73
Revises: ec25e5cb1147
Create Date: 2017-11-16 17:54:23.396524

"""

# revision identifiers, used by Alembic.
revision = '6f01ba0dbd73'
down_revision = 'ec25e5cb1147'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_dates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('to_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('create_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('update_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('delete_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('work_dates1')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_dates1',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('from_time', sa.DATETIME(), nullable=False),
    sa.Column('to_time', sa.DATETIME(), nullable=True),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.Column('create_date', sa.DATETIME(), nullable=False),
    sa.Column('update_date', sa.DATETIME(), nullable=True),
    sa.Column('delete_date', sa.DATETIME(), nullable=True),
    sa.Column('deleted', sa.BOOLEAN(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('work_dates')
    ### end Alembic commands ###
