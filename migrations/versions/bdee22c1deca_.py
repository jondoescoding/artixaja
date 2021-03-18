"""empty message

Revision ID: bdee22c1deca
Revises: a35df4f4b179
Create Date: 2021-03-03 02:39:06.471656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdee22c1deca'
down_revision = 'a35df4f4b179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory', 'stocklevel')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('stocklevel', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###