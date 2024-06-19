"""add content column to posts table

Revision ID: 2b34f8176e33
Revises: efb717f16b83
Create Date: 2024-06-18 10:34:30.533670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b34f8176e33'
down_revision: Union[str, None] = 'df6f6c252aed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String, nullable=False) )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
