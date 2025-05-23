"""empty message

Revision ID: 45f78cd2e6cf
Revises: bbaafd032844
Create Date: 2024-08-29 03:06:53.251953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45f78cd2e6cf'
down_revision = 'bbaafd032844'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match_analysis', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('admin')

    with op.batch_alter_table('match_analysis', schema=None) as batch_op:
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###
