"""add some sequence to oracle db

Revision ID: 62404fa16786
Revises: 72b7fad92f97
Create Date: 2025-02-02 17:32:45.681099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62404fa16786'
down_revision = '72b7fad92f97'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # List of models without 'oog' prefix
    models = [
        'top_bar_menu',
        'side_bar_menu',
        'menu_item_permission'
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
        'top_bar_menu',
        'side_bar_menu',
        'menu_item_permission'
    ]
    
    for model_name in models:
        seq_name = "%s_id_seq"%model_name
        table_name = "oog_%s"%model_name
        trigger_name = "%s_bfi"%model_name # bfi = before insert

        # Step 1: Drop the trigger
        op.execute(f"DROP TRIGGER {trigger_name}")
        
        # Step 2: Drop the sequence
        op.execute(sa.schema.DropSequence(sa.Sequence(seq_name)))

