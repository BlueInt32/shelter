"""empty message

Revision ID: 86deeef72b9c
Revises: 0fc9a6329571
Create Date: 2020-05-03 16:59:08.004469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86deeef72b9c'
down_revision = '0fc9a6329571'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('element', sa.Column('type', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('element', 'type')
    # ### end Alembic commands ###
