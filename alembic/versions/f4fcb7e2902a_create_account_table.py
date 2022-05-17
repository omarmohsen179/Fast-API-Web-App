"""create account table

Revision ID: f4fcb7e2902a
Revises: 38c3da42c065
Create Date: 2022-05-15 01:05:27.348858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4fcb7e2902a'
down_revision = '38c3da42c065'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Appuser', sa.Column('LastPasswordReset', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Appuser', 'LastPasswordReset')
    # ### end Alembic commands ###
