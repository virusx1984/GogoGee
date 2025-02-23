"""update menu sys

Revision ID: 3b6954efd35e
Revises: ad9762760f96
Create Date: 2025-02-02 10:26:14.798963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b6954efd35e'
down_revision = 'ad9762760f96'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oog_top_bar_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oog_side_bar_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('top_bar_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['oog_side_bar_menu.id'], ),
    sa.ForeignKeyConstraint(['top_bar_id'], ['oog_top_bar_menu.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oog_menu_item_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['menu_id'], ['oog_side_bar_menu.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['oog_permission.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oog_menu_item_permission')
    op.drop_table('oog_side_bar_menu')
    op.drop_table('oog_top_bar_menu')
    # ### end Alembic commands ###
