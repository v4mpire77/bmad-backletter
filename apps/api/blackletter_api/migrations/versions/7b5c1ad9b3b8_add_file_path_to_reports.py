"""add file_path to reports"""

from alembic import op
import sqlalchemy as sa

revision = "7b5c1ad9b3b8"
down_revision = "c4b32e6c5a41"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("reports", sa.Column("file_path", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("reports", "file_path")
