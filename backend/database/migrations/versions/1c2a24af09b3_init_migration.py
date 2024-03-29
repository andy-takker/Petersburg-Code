"""Init migration

Revision ID: 1c2a24af09b3
Revises: 
Create Date: 2022-07-27 07:50:52.637629

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import datetime


# revision identifiers, used by Alembic.
from database import PaymentType

revision = '1c2a24af09b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('directivity',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=127), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_directivity_id'), 'directivity', ['id'], unique=False)
    op.create_index(op.f('ix_directivity_name'), 'directivity', ['name'], unique=False)
    op.create_table('organization',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organization_id'), 'organization', ['id'], unique=False)
    op.create_index(op.f('ix_organization_name'), 'organization', ['name'], unique=False)
    op.create_table('source',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=False),
    sa.Column('enable', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_source_id'), 'source', ['id'], unique=False)
    op.create_table('study_area',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_area_id'), 'study_area', ['id'], unique=False)
    op.create_index(op.f('ix_study_area_name'), 'study_area', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('career_test',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('suitable_profession', sa.String(length=255), nullable=False),
    sa.Column('match_percentage', sa.Float(), nullable=False),
    sa.Column('data', sa.PickleType(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_career_test_id'), 'career_test', ['id'], unique=False)
    op.create_index(op.f('ix_career_test_match_percentage'), 'career_test', ['match_percentage'], unique=False)
    op.create_index(op.f('ix_career_test_suitable_profession'), 'career_test', ['suitable_profession'], unique=False)
    op.create_index(op.f('ix_career_test_user_id'), 'career_test', ['user_id'], unique=False)
    op.create_table('event',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('source_url', sqlalchemy_utils.types.url.URLType(), nullable=False),
    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=True, comment='Сайт конкурса'),
    sa.Column('published_date', sa.DateTime(timezone=datetime.timezone.utc), nullable=True, comment='Дата публикации'),
    sa.Column('deadline_date', sa.DateTime(), nullable=True, comment='Дата дедлайна'),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('source_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_id'), 'event', ['id'], unique=False)
    op.create_index(op.f('ix_event_source_id'), 'event', ['source_id'], unique=False)
    op.create_table('program',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('organization_id', sa.BigInteger(), nullable=False),
    sa.Column('directivity_id', sa.BigInteger(), nullable=False),
    sa.Column('payment', sqlalchemy_utils.types.choice.ChoiceType(PaymentType, impl=sa.String(255)), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.Column('group_with_online_signup_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['directivity_id'], ['directivity.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_program_directivity_id'), 'program', ['directivity_id'], unique=False)
    op.create_index(op.f('ix_program_id'), 'program', ['id'], unique=False)
    op.create_index(op.f('ix_program_organization_id'), 'program', ['organization_id'], unique=False)
    op.create_table('study_area_program',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('program_id', sa.BigInteger(), nullable=False),
    sa.Column('study_area_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    sa.ForeignKeyConstraint(['study_area_id'], ['study_area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_area_program_id'), 'study_area_program', ['id'], unique=False)
    op.create_index(op.f('ix_study_area_program_program_id'), 'study_area_program', ['program_id'], unique=False)
    op.create_index(op.f('ix_study_area_program_study_area_id'), 'study_area_program', ['study_area_id'], unique=False)
    op.create_table('user_event',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.Column('is_involved', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'event_id')
    )
    op.create_index(op.f('ix_user_event_event_id'), 'user_event', ['event_id'], unique=False)
    op.create_index(op.f('ix_user_event_id'), 'user_event', ['id'], unique=False)
    op.create_index(op.f('ix_user_event_user_id'), 'user_event', ['user_id'], unique=False)
    op.create_table('celery_crontab_schedule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('minute', sa.String(length=240), nullable=True),
    sa.Column('hour', sa.String(length=96), nullable=True),
    sa.Column('day_of_week', sa.String(length=64), nullable=True),
    sa.Column('day_of_month', sa.String(length=124), nullable=True),
    sa.Column('month_of_year', sa.String(length=64), nullable=True),
    sa.Column('timezone', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_table('celery_interval_schedule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('every', sa.Integer(), nullable=False),
    sa.Column('period', sa.String(length=24), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_table('celery_periodic_task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('task', sa.String(length=255), nullable=True),
    sa.Column('interval_id', sa.Integer(), nullable=True),
    sa.Column('crontab_id', sa.Integer(), nullable=True),
    sa.Column('solar_id', sa.Integer(), nullable=True),
    sa.Column('args', sa.Text(), nullable=True),
    sa.Column('kwargs', sa.Text(), nullable=True),
    sa.Column('queue', sa.String(length=255), nullable=True),
    sa.Column('exchange', sa.String(length=255), nullable=True),
    sa.Column('routing_key', sa.String(length=255), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('expires', sa.DateTime(timezone=True), nullable=True),
    sa.Column('one_off', sa.Boolean(), nullable=True),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('total_run_count', sa.Integer(), nullable=False),
    sa.Column('date_changed', sa.DateTime(timezone=True), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sqlite_autoincrement=True
    )
    op.create_table('celery_periodic_task_changed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_update', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('celery_solar_schedule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('event', sa.String(length=24), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('celery_solar_schedule')
    op.drop_table('celery_periodic_task_changed')
    op.drop_table('celery_periodic_task')
    op.drop_table('celery_interval_schedule')
    op.drop_table('celery_crontab_schedule')
    op.drop_index(op.f('ix_user_event_user_id'), table_name='user_event')
    op.drop_index(op.f('ix_user_event_id'), table_name='user_event')
    op.drop_index(op.f('ix_user_event_event_id'), table_name='user_event')
    op.drop_table('user_event')
    op.drop_index(op.f('ix_study_area_program_study_area_id'), table_name='study_area_program')
    op.drop_index(op.f('ix_study_area_program_program_id'), table_name='study_area_program')
    op.drop_index(op.f('ix_study_area_program_id'), table_name='study_area_program')
    op.drop_table('study_area_program')
    op.drop_index(op.f('ix_program_organization_id'), table_name='program')
    op.drop_index(op.f('ix_program_id'), table_name='program')
    op.drop_index(op.f('ix_program_directivity_id'), table_name='program')
    op.drop_table('program')
    op.drop_index(op.f('ix_event_source_id'), table_name='event')
    op.drop_index(op.f('ix_event_id'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_career_test_user_id'), table_name='career_test')
    op.drop_index(op.f('ix_career_test_suitable_profession'), table_name='career_test')
    op.drop_index(op.f('ix_career_test_match_percentage'), table_name='career_test')
    op.drop_index(op.f('ix_career_test_id'), table_name='career_test')
    op.drop_table('career_test')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_study_area_name'), table_name='study_area')
    op.drop_index(op.f('ix_study_area_id'), table_name='study_area')
    op.drop_table('study_area')
    op.drop_index(op.f('ix_source_id'), table_name='source')
    op.drop_table('source')
    op.drop_index(op.f('ix_organization_name'), table_name='organization')
    op.drop_index(op.f('ix_organization_id'), table_name='organization')
    op.drop_table('organization')
    op.drop_index(op.f('ix_directivity_name'), table_name='directivity')
    op.drop_index(op.f('ix_directivity_id'), table_name='directivity')
    op.drop_table('directivity')
    # ### end Alembic commands ###
