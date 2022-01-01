"""create book table

Revision ID: 02b27e674ea7
Revises:
Create Date: 2022-01-01 18:12:39.090629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02b27e674ea7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'book',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('isbn', sa.String(17), unique=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('page', sa.Integer, nullable=False),
        sa.Column('read_page', sa.Integer, nullable=False, default=0),
        sa.Column('created_at', sa.Integer, index=True, nullable=False),
        sa.Column('updated_at', sa.Integer, index=True, nullable=False),
    )

def downgrade():
    op.drop_table('book')
