"""empty message

Revision ID: d0de71e842cf
Revises: 
Create Date: 2023-02-14 20:38:56.910060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0de71e842cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
   pass

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contemporaries', schema=None) as batch_op:
        batch_op.drop_constraint('unique_contemporaries', type_='unique')

    # ### end Alembic commands ###