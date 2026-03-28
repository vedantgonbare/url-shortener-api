"""add_user_id_to_urls

Revision ID: a3e0c3fdefe0
Revises: b5b1accafd1d
Create Date: 2026-03-28 09:32:27.998742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3e0c3fdefe0'
down_revision: Union[str, Sequence[str], None] = 'b5b1accafd1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('urls',
        sa.Column('user_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_urls_user_id', 'urls', 'users', ['user_id'], ['id']
    )

def downgrade() -> None:
    op.drop_constraint('fk_urls_user_id', 'urls', type_='foreignkey')
    op.drop_column('urls', 'user_id')
