"""Initial migration.

Revision ID: fc81ae659ef3
Revises: 0432e5dfc213
Create Date: 2024-11-28 00:24:24.316370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc81ae659ef3'
down_revision = '0432e5dfc213'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_game_room')
    op.drop_table('resource')
    op.drop_table('inventory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###