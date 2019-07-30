"""refactor phone models

Revision ID: d19820fc3341
Revises: 9fe7f8aa7849
Create Date: 2019-06-03 12:24:38.858805

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd19820fc3341'
down_revision = '9fe7f8aa7849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phone_contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # ----- data migration -----
    connection = op.get_bind()
    migration_query1 = sa.sql.text('''
        INSERT INTO phone_contact (
            participant_id, number, uuid, created, updated, verified)
        SELECT pp.participant_id, ph.number, ph.uuid,
            current_timestamp, pp.last_seen, pp.verified
        FROM participant_phone AS pp JOIN phone AS ph
        ON pp.phone_id = ph.id;
    ''')
    connection.execute(migration_query1)
    # ----- data migration -----

    op.drop_table('participant_phone')
    op.drop_table('phone')
    op.add_column(
        'submission', sa.Column('last_phone_number', sa.String(),
        nullable=True))

    # ----- data migration -----
    migration_query2 = sa.sql.text('''
        WITH sel1 AS (
            SELECT DISTINCT ON (submission_id) submission_id, sender
            FROM message WHERE direction = 'IN' and submission_id IS NOT NULL
            ORDER BY submission_id, received DESC
        )
        UPDATE submission SET last_phone_number = sel1.sender FROM sel1
        WHERE submission.id = sel1.submission_id;
    ''')
    connection.execute(migration_query2)
    # ----- data migration -----
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phone',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('number', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='phone_pkey'),
    sa.UniqueConstraint('number', name='phone_number_key')
    )
    op.drop_column('submission', 'last_phone_number')
    op.create_table('participant_phone',
    sa.Column('participant_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('phone_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('last_seen', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('verified', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], name='participant_phone_participant_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['phone_id'], ['phone.id'], name='participant_phone_phone_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('participant_id', 'phone_id', name='participant_phone_pkey')
    )

    # ----- data migration -----
    connection = op.get_bind()
    migration_query = sa.sql.text('''
        WITH ins1 AS (
            INSERT INTO phone (number, uuid)
            SELECT DISTINCT ON (number) number, uuid FROM phone_contact
            ORDER BY number DESC, updated DESC
            RETURNING id AS phone_id, uuid as phone_uuid
        )
        INSERT INTO participant_phone (
            participant_id, phone_id, last_seen, uuid, verified
        ) SELECT pc.participant_id, ins1.phone_id, pc.updated, pc.uuid,
            pc.verified FROM phone_contact AS pc JOIN ins1 ON
            ins1.phone_uuid = pc.uuid;
    ''')
    connection.execute(migration_query)
    # ----- data migration -----

    op.drop_table('phone_contact')
    # ### end Alembic commands ###