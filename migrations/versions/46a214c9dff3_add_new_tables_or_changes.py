"""Add new tables or changes

Revision ID: 46a214c9dff3
Revises: 762ed12ed483
Create Date: 2024-11-28 11:57:49.998179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46a214c9dff3'
down_revision = '762ed12ed483'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('saved_game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('game_room_state', sa.JSON(), nullable=False),
    sa.Column('player_states', sa.JSON(), nullable=False),
    sa.Column('inventory', sa.JSON(), nullable=False),
    sa.Column('resources', sa.JSON(), nullable=False),
    sa.Column('saved_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saved_game')
    # ### end Alembic commands ###
