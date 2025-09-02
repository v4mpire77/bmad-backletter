"""add compliance and llm flags to org settings"""

from alembic import op
import sqlalchemy as sa

revision = "8b6e5f4c2a71"
down_revision = "c4b32e6c5a41"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "org_settings",
        sa.Column(
            "compliance_mode",
            sa.Enum("strict", "standard", name="compliancemode"),
            nullable=False,
            server_default="strict",
        ),
    )
    op.add_column(
        "org_settings",
        sa.Column("evidence_window", sa.Integer(), nullable=False, server_default="2"),
    )
    op.add_column(
        "org_settings",
        sa.Column("llm_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )



def downgrade() -> None:
    op.drop_column("org_settings", "llm_enabled")
    op.drop_column("org_settings", "evidence_window")
    op.drop_column("org_settings", "compliance_mode")
    sa.Enum(name="compliancemode").drop(op.get_bind())

