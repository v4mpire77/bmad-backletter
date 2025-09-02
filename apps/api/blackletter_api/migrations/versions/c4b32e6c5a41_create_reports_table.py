"""create reports table"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "c4b32e6c5a41"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("analysis_id", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("options", sa.JSON(), nullable=False),
    )
    op.create_index(op.f("ix_reports_analysis_id"), "reports", ["analysis_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_reports_analysis_id"), table_name="reports")
    op.drop_table("reports")
