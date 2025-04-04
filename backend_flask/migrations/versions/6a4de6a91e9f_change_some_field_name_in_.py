"""change some field name in MenuItemPermission and SideBarMenu

Revision ID: 6a4de6a91e9f
Revises: 62404fa16786
Create Date: 2025-02-02 23:23:23.102911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a4de6a91e9f'
down_revision = '62404fa16786'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oog_menu_item_permission', sa.Column('side_bar_menu_id', sa.Integer(), nullable=True))
    op.drop_constraint('sys_c0011367', 'oog_menu_item_permission', type_='foreignkey')
    op.create_foreign_key(None, 'oog_menu_item_permission', 'oog_side_bar_menu', ['side_bar_menu_id'], ['id'])
    op.drop_column('oog_menu_item_permission', 'menu_id')
    op.add_column('oog_side_bar_menu', sa.Column('top_bar_menu_id', sa.Integer(), nullable=True))
    op.drop_constraint('sys_c0011362', 'oog_side_bar_menu', type_='foreignkey')
    op.create_foreign_key(None, 'oog_side_bar_menu', 'oog_top_bar_menu', ['top_bar_menu_id'], ['id'])
    op.drop_column('oog_side_bar_menu', 'top_bar_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oog_side_bar_menu', sa.Column('top_bar_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'oog_side_bar_menu', type_='foreignkey')
    op.create_foreign_key('sys_c0011362', 'oog_side_bar_menu', 'oog_top_bar_menu', ['top_bar_id'], ['id'])
    op.drop_column('oog_side_bar_menu', 'top_bar_menu_id')
    op.add_column('oog_menu_item_permission', sa.Column('menu_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'oog_menu_item_permission', type_='foreignkey')
    op.create_foreign_key('sys_c0011367', 'oog_menu_item_permission', 'oog_side_bar_menu', ['menu_id'], ['id'])
    op.drop_column('oog_menu_item_permission', 'side_bar_menu_id')
    # ### end Alembic commands ###
