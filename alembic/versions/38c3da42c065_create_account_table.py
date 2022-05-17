"""create account table

Revision ID: 38c3da42c065
Revises: a77d6ad21a6e
Create Date: 2022-05-15 01:04:07.533741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38c3da42c065'
down_revision = 'a77d6ad21a6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Appuser', 'LastPasswordReset')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Appuser', sa.Column('LastPasswordReset', sa.DATE(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
