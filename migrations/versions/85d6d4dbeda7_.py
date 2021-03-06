"""empty message

Revision ID: 85d6d4dbeda7
Revises: 8a5eddd14399
Create Date: 2019-06-06 23:15:19.691927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d6d4dbeda7'
down_revision = '8a5eddd14399'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('failed_access_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attempted_uid', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_failed_access_logs_created_at'), 'failed_access_logs', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_failed_access_logs_created_at'), table_name='failed_access_logs')
    op.drop_table('failed_access_logs')
    # ### end Alembic commands ###
