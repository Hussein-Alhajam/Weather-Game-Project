"""Initial migration.

Revision ID: 0b41e7296560
Revises: 
Create Date: 2024-11-28 07:26:18.114722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b41e7296560'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_name', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('room_name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('game_room_state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('last_transition', sa.DateTime(), nullable=True),
    sa.Column('current_state', sa.String(length=20), nullable=True),
    sa.Column('cycle_duration', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['game_room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player_state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('hunger_level', sa.Float(), nullable=True),
    sa.Column('health_level', sa.Float(), nullable=True),
    sa.Column('sanity_level', sa.Float(), nullable=True),
    sa.Column('stamina_level',sa.Float(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
    'resource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=80), nullable=False),  # e.g., wood, stone
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('location_x', sa.Float(), nullable=True),
    sa.Column('location_y', sa.Float(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['game_room.id']),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
    'inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.Column('item_name', sa.String(length=80), nullable=True),  # Crafted items
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id']),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id']),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
    'user_game_room',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id']),
    sa.ForeignKeyConstraint(['room_id'], ['game_room.id']),
    sa.PrimaryKeyConstraint('user_id', 'room_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_game_room')
    op.drop_table('inventory')
    op.drop_table('resource')
    op.drop_table('player_state')
    op.drop_table('user')
    op.drop_table('game_room_state')
    op.drop_table('game_room')
    # ### end Alembic commands ###