"""Add new tables or changes

Revision ID: b1e3141e85da
Revises: 0b41e7296560
Create Date: 2024-11-28 07:51:14.507884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e3141e85da'
down_revision = '0b41e7296560'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventory')
    op.drop_table('user_game_room')
    op.drop_table('resource')
    with op.batch_alter_table('player_state', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sanity_level', sa.Float(), nullable=True))
        batch_op.drop_column('stamina_level')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player_state', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stamina_level', sa.FLOAT(), nullable=True))
        batch_op.drop_column('sanity_level')

    op.create_table('resource',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('type', sa.VARCHAR(length=80), nullable=False),
    sa.Column('quantity', sa.INTEGER(), nullable=True),
    sa.Column('location_x', sa.FLOAT(), nullable=True),
    sa.Column('location_y', sa.FLOAT(), nullable=True),
    sa.Column('room_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['game_room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_game_room',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('room_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['game_room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'room_id')
    )
    op.create_table('inventory',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('resource_id', sa.INTEGER(), nullable=True),
    sa.Column('item_name', sa.VARCHAR(length=80), nullable=True),
    sa.Column('quantity', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
