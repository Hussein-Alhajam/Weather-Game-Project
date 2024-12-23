"""Add new tables or changes

Revision ID: 0a6188e67b9b
Revises: b1e3141e85da
Create Date: 2024-11-28 09:20:10.591463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a6188e67b9b'
down_revision = 'b1e3141e85da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player_state', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stamina_level', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player_state', schema=None) as batch_op:
        batch_op.drop_column('stamina_level')

    # ### end Alembic commands ###
