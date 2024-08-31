"""remove image url

Revision ID: f0a02af9d33f
Revises: c6f1226eb52b
Create Date: 2024-08-31 09:03:10.079784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0a02af9d33f'
down_revision: Union[str, None] = 'c6f1226eb52b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'image_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###