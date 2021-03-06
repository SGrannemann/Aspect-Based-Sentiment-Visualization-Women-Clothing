"""initial setup

Revision ID: 225814207627
Revises: 
Create Date: 2022-01-23 08:59:00.596251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '225814207627'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_query',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userquery', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_query')
    # ### end Alembic commands ###
