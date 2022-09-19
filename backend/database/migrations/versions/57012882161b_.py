"""empty message

Revision ID: 57012882161b
Revises: df90c2902d23
Create Date: 2022-09-16 23:34:13.872405

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import datetime


# revision identifiers, used by Alembic.
revision = '57012882161b'
down_revision = 'df90c2902d23'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'education_profile',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_education_profile_id'), 'education_profile', ['id'], unique=False)
    op.create_index(op.f('ix_education_profile_name'), 'education_profile', ['name'], unique=False)
    op.create_table(
        'education_profile_program',
        sa.Column('program_id', sa.BigInteger(), nullable=False),
        sa.Column('education_profile_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['education_profile_id'], ['education_profile.id'], ),
        sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    )
    op.create_index(op.f('ix_education_profile_program_education_profile_id'), 'education_profile_program', ['education_profile_id'], unique=False)
    op.create_index(op.f('ix_education_profile_program_program_id'), 'education_profile_program', ['program_id'], unique=False)
    op.drop_index('ix_study_area_program_id', table_name='study_area_program')
    op.drop_column('study_area_program', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('study_area_program', sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False))
    op.create_index('ix_study_area_program_id', 'study_area_program', ['id'], unique=False)
    op.drop_index(op.f('ix_education_profile_program_program_id'), table_name='education_profile_program')
    op.drop_index(op.f('ix_education_profile_program_education_profile_id'), table_name='education_profile_program')
    op.drop_table('education_profile_program')
    op.drop_index(op.f('ix_education_profile_name'), table_name='education_profile')
    op.drop_index(op.f('ix_education_profile_id'), table_name='education_profile')
    op.drop_table('education_profile')
    # ### end Alembic commands ###
