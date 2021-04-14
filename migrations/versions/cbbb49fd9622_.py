"""empty message

Revision ID: cbbb49fd9622
Revises: 54d4cf48580c
Create Date: 2021-04-12 00:11:00.075542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbbb49fd9622'
down_revision = '54d4cf48580c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'categories', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'categories', type_='unique')
    # ### end Alembic commands ###
