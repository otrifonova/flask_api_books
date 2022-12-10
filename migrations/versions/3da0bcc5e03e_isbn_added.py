"""isbn_added

Revision ID: 3da0bcc5e03e
Revises: cf6d2bac65b0
Create Date: 2022-12-04 16:31:41.561799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3da0bcc5e03e'
down_revision = 'cf6d2bac65b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('edition', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isbn', sa.String(), nullable=True))
        batch_op.create_unique_constraint(None, ['isbn'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('edition', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('isbn')

    # ### end Alembic commands ###
