"""create comment

Revision ID: 35acfab584de
Revises: ac77615e5716
Create Date: 2023-06-26 03:33:59.675773

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '35acfab584de'
down_revision = 'ac77615e5716'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('text', sa.String(length=500), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('announcement_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['announcement_id'], ['announcement.id'], name='fk_comment_announcement_id_announcement'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_comment_user_id_user'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
