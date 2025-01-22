"""add sequences of id of every model

Revision ID: 57d8c92ddd75
Revises: 4126435e5018
Create Date: 2025-01-23 00:09:25.330433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57d8c92ddd75'
down_revision = '4126435e5018'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # List of models without 'oog' prefix
    models = [
        'location',
        'company',
        'bg',
        'bu',
        'plant_district',
        'plant',
        'supplier',
        'supplier_pod',
        'currency_ex',
        'machine',
        'asset',
        'customer',
        'shipping_site',
        'product',
        'product_share_ver',
        'pdbu_product',
        'yield_rate',
        'part_num',
        'pn_layer',
        'proc_code',
        'sub_proc_code',
        'pn_layer_proc',
        'pn_layer_sproc',
        'role',
        'user_role',
        'user',
        'permission',
        'role_permission',
        'material',
        'sproc_material'
    ]

    
    for model_name in models:
        seq_name = "%s_id_seq"%model_name
        table_name = "oog_%s"%model_name
        trigger_name = "%s_bfi"%model_name # bfi = before insert

        # Step 1: Create the sequence
        op.execute(sa.schema.CreateSequence(sa.Sequence(seq_name)))
        
        # Step 2: Create the trigger
        trigger_sql = f"""
            CREATE OR REPLACE TRIGGER {trigger_name}
            BEFORE INSERT ON {table_name}
            FOR EACH ROW
            BEGIN
                IF :NEW.id IS NULL THEN
                    SELECT {seq_name}.NEXTVAL INTO :NEW.id FROM dual;
                END IF;
            END;
            """
        op.get_bind().exec_driver_sql(trigger_sql)

def downgrade() -> None:
    # List of models without 'oog' prefix
    models = [
        'location',
        'company',
        'bg',
        'bu',
        'plant_district',
        'plant',
        'supplier',
        'supplier_pod',
        'currency_ex',
        'machine',
        'asset',
        'customer',
        'shipping_site',
        'product',
        'product_share_ver',
        'pdbu_product',
        'yield_rate',
        'part_num',
        'pn_layer',
        'proc_code',
        'sub_proc_code',
        'pn_layer_proc',
        'pn_layer_sproc',
        'role',
        'user_role',
        'user',
        'permission',
        'role_permission',
        'material',
        'sproc_material'
    ]
    
    # No operations needed since we're just maintaining the model list
    for model_name in models:
        seq_name = "%s_id_seq"%model_name
        table_name = "oog_%s"%model_name
        trigger_name = "%s_bfi"%model_name # bfi = before insert

        # Step 1: Drop the trigger
        op.execute(f"DROP TRIGGER {trigger_name}")
        
        # Step 2: Drop the sequence
        op.execute(sa.schema.DropSequence(sa.Sequence(seq_name)))
