"""empty message

Revision ID: 214bc099ec3d
Revises: 0b77bedb6de1
Create Date: 2022-05-12 09:50:03.487622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '214bc099ec3d'
down_revision = '0b77bedb6de1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
