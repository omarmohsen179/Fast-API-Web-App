"""omar32142

Revision ID: ec566f9b5336
Revises: 513f6b9481e1
Create Date: 2022-03-17 13:35:03.587955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec566f9b5336'
down_revision = '513f6b9481e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Item',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_index(op.f('ix_Item_Id'), 'Item', ['Id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Item_Id'), table_name='Item')
    op.drop_table('Item')
    # ### end Alembic commands ###
