"""add tables

Revision ID: 24c02226b72e
Revises: b211289f00fd
Create Date: 2024-12-22 23:43:50.518366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24c02226b72e'
down_revision = 'b211289f00fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oog_machine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('supplier_pod_id', sa.Integer(), nullable=True),
    sa.Column('proxy_supplier_pod_id', sa.Integer(), nullable=True),
    sa.Column('plant_id', sa.Integer(), nullable=True),
    sa.Column('floor', sa.Float(), nullable=True),
    sa.Column('coordx', sa.Float(), nullable=True),
    sa.Column('coordy', sa.Float(), nullable=True),
    sa.Column('m_length', sa.Float(), nullable=True),
    sa.Column('m_width', sa.Float(), nullable=True),
    sa.Column('m_height', sa.Float(), nullable=True),
    sa.Column('cover_length', sa.Float(), nullable=True),
    sa.Column('cover_width', sa.Float(), nullable=True),
    sa.Column('standard_name', sa.String(length=100), nullable=True),
    sa.Column('verbose_name', sa.String(length=100), nullable=True),
    sa.Column('m_model', sa.String(length=100), nullable=True),
    sa.Column('verbose_num', sa.Integer(), nullable=True),
    sa.Column('detail_info', sa.Text(), nullable=True),
    sa.Column('acuisition_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['plant_id'], ['oog_plant.id'], ),
    sa.ForeignKeyConstraint(['proxy_supplier_pod_id'], ['oog_supplier_pod.id'], ),
    sa.ForeignKeyConstraint(['supplier_pod_id'], ['oog_supplier_pod.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oog_machine')
    # ### end Alembic commands ###