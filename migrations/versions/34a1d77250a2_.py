"""empty message

Revision ID: 34a1d77250a2
Revises: 26be248c4cde
Create Date: 2018-11-30 20:08:49.273346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34a1d77250a2'
down_revision = '26be248c4cde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ais',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uploaded_on', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename')
    )
    op.create_table('game_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('is_draw', sa.Boolean(), nullable=True),
    sa.Column('ai_won_id', sa.Integer(), nullable=False),
    sa.Column('ai_lost_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ai_lost_id'], ['ais.id'], ),
    sa.ForeignKeyConstraint(['ai_won_id'], ['ais.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_logs_timestamp'), 'game_logs', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game_logs_timestamp'), table_name='game_logs')
    op.drop_table('game_logs')
    op.drop_table('ais')
    # ### end Alembic commands ###