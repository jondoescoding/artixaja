"""empty message

Revision ID: 583bfebbf754
Revises: 18f4cfa1a7e7
Create Date: 2021-04-12 00:14:05.358833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '583bfebbf754'
down_revision = '18f4cfa1a7e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('cost', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory', 'cost')
    # ### end Alembic commands ###
