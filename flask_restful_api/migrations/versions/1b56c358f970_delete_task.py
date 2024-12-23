"""delete task

Revision ID: 1b56c358f970
Revises: 303fe5ae496b
Create Date: 2024-12-20 21:53:28.428187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b56c358f970'
down_revision = '303fe5ae496b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=100), nullable=False),
    sa.Column('description2', sa.VARCHAR(length=100), nullable=False),
    sa.Column('completed', sa.INTEGER(), nullable=True),
    sa.Column('fullname', sa.VARCHAR(length=120), nullable=True),
    sa.Column('othername', sa.VARCHAR(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id', name='sys_c0010981')
    )
    # ### end Alembic commands ###
