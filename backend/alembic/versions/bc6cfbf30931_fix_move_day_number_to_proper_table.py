"""fix: move day_number to proper table

Revision ID: bc6cfbf30931
Revises: 142f79db6dc2
Create Date: 2025-03-18 03:04:41.402231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc6cfbf30931'
down_revision: Union[str, None] = '142f79db6dc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('day_of_week', sa.Column('day_number', sa.Integer(), nullable=False, comment='Numeric representation of day of week (e.g., 1=Monday, 2=Tuesday, ...)'))
    op.create_unique_constraint(None, 'day_of_week', ['day_number'])
    op.drop_constraint('week_types_day_number_key', 'week_types', type_='unique')
    op.drop_column('week_types', 'day_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('week_types', sa.Column('day_number', sa.INTEGER(), autoincrement=False, nullable=False, comment='Numeric representation of day of week (e.g., 1=Monday, 2=Tuesday, ...)'))
    op.create_unique_constraint('week_types_day_number_key', 'week_types', ['day_number'])
    op.drop_constraint(None, 'day_of_week', type_='unique')
    op.drop_column('day_of_week', 'day_number')
    # ### end Alembic commands ###
