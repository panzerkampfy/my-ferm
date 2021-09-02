"""Added storage model

Revision ID: 77ee92002451
Revises: 33db04ac8224
Create Date: 2021-09-02 12:22:07.214372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77ee92002451'
down_revision = '33db04ac8224'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storage',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('count', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_storage_id'), 'storage', ['id'], unique=False)
    op.create_table('storage_jobs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('storage_id', sa.INTEGER(), nullable=True),
    sa.Column('job_id', sa.INTEGER(), nullable=True),
    sa.Column('count', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['storage_id'], ['storage.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_storage_jobs_id'), 'storage_jobs', ['id'], unique=False)
    op.add_column('jobs', sa.Column('product_zone_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'jobs', 'product_zone', ['product_zone_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'jobs', type_='foreignkey')
    op.drop_column('jobs', 'product_zone_id')
    op.drop_index(op.f('ix_storage_jobs_id'), table_name='storage_jobs')
    op.drop_table('storage_jobs')
    op.drop_index(op.f('ix_storage_id'), table_name='storage')
    op.drop_table('storage')
    # ### end Alembic commands ###
