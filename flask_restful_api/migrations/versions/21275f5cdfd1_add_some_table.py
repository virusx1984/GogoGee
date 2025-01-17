"""add some table

Revision ID: 21275f5cdfd1
Revises: 8da4ec355dba
Create Date: 2025-01-18 00:27:55.345334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21275f5cdfd1'
down_revision = '8da4ec355dba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oog_audit_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(length=50), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oog_menu_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True, comment='menu item name'),
    sa.Column('icon', sa.String(length=50), nullable=True, comment='optional icon class'),
    sa.Column('route', sa.String(length=100), nullable=True, comment='route path'),
    sa.Column('order', sa.Integer(), nullable=True, comment='display order'),
    sa.Column('parent_id', sa.Integer(), nullable=True, comment='foreign key to parent menu item'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='controls visibility'),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['oog_menu_item.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Represents a single menu item in the hierarchical menu system'
    )
    op.create_table('oog_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oog_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oog_user_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('session_created_dt', sa.DateTime(), nullable=True),
    sa.Column('session_expires_dt', sa.DateTime(), nullable=True),
    sa.Column('last_activity', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oog_menu_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('menu_item_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['menu_item_id'], ['oog_menu_item.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['oog_permission.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Links menu items to permissions'
    )
    op.create_table('oog_role_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['oog_permission.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['oog_role.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oog_user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('updated_dt', sa.DateTime(), nullable=True),
    sa.Column('created_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_user_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['oog_role.id'], ),
    sa.ForeignKeyConstraint(['updated_user_id'], ['oog_user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['oog_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('oog_user', sa.Column('created_dt', sa.DateTime(), nullable=True))
    op.add_column('oog_user', sa.Column('updated_dt', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('oog_user', 'updated_dt')
    op.drop_column('oog_user', 'created_dt')
    op.drop_table('oog_user_role')
    op.drop_table('oog_role_permission')
    op.drop_table('oog_menu_permission')
    op.drop_table('oog_user_session')
    op.drop_table('oog_role')
    op.drop_table('oog_permission')
    op.drop_table('oog_menu_item')
    op.drop_table('oog_audit_log')
    # ### end Alembic commands ###
