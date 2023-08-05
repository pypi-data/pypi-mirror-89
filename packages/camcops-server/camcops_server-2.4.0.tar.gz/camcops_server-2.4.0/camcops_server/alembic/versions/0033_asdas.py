#!/usr/bin/env python

"""
camcops_server/alembic/versions/0033.py

===============================================================================

    Copyright (C) 2012-2020 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CamCOPS.

    CamCOPS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CamCOPS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CamCOPS. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

DATABASE REVISION SCRIPT

asdas

Revision ID: 0033
Revises: 0032
Creation date: 2019-07-15 15:08:49.770711

"""

# =============================================================================
# Imports
# =============================================================================

from alembic import op
import sqlalchemy as sa
import camcops_server.cc_modules.cc_sqla_coltypes


# =============================================================================
# Revision identifiers, used by Alembic.
# =============================================================================

revision = '0033'
down_revision = '0032'
branch_labels = None
depends_on = None


# =============================================================================
# The upgrade/downgrade steps
# =============================================================================

# noinspection PyPep8,PyTypeChecker
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('asdas',
    sa.Column('q1', sa.Integer(), nullable=True, comment='Q1 - back pain 0-10 (None - very severe)'),
    sa.Column('q2', sa.Integer(), nullable=True, comment='Q2 - morning stiffness 0-10 (None - 2+ hours)'),
    sa.Column('q3', sa.Integer(), nullable=True, comment='Q3 - patient global 0-10 (Not active - very active)'),
    sa.Column('q4', sa.Integer(), nullable=True, comment='Q4 - peripheral pain 0-10 (None - very severe)'),
    sa.Column('q5', sa.Float(), nullable=True, comment='CRP (mg/L)'),
    sa.Column('q6', sa.Float(), nullable=True, comment='ESR (mm/h)'),
    sa.Column('patient_id', sa.Integer(), nullable=False, comment='(TASK) Foreign key to patient.id (for this device/era)'),
    sa.Column('clinician_specialty', sa.Text(), nullable=True, comment="(CLINICIAN) Clinician's specialty (e.g. Liaison Psychiatry)"),
    sa.Column('clinician_name', sa.Text(), nullable=True, comment="(CLINICIAN) Clinician's name (e.g. Dr X)"),
    sa.Column('clinician_professional_registration', sa.Text(), nullable=True, comment="(CLINICIAN) Clinician's professional registration (e.g. GMC# 12345)"),
    sa.Column('clinician_post', sa.Text(), nullable=True, comment="(CLINICIAN) Clinician's post (e.g. Consultant)"),
    sa.Column('clinician_service', sa.Text(), nullable=True, comment="(CLINICIAN) Clinician's service (e.g. Liaison Psychiatry Service)"),
    sa.Column('clinician_contact_details', sa.Text(), nullable=True, comment="(CLINICIAN) Clinician's contact details (e.g. bleep, extension)"),
    sa.Column('when_created', camcops_server.cc_modules.cc_sqla_coltypes.PendulumDateTimeAsIsoTextColType(length=32), nullable=False, comment='(TASK) Date/time this task instance was created (ISO 8601)'),
    sa.Column('when_firstexit', camcops_server.cc_modules.cc_sqla_coltypes.PendulumDateTimeAsIsoTextColType(length=32), nullable=True, comment='(TASK) Date/time of the first exit from this task (ISO 8601)'),
    sa.Column('firstexit_is_finish', sa.Boolean(), nullable=True, comment='(TASK) Was the first exit from the task because it was finished (1)?'),
    sa.Column('firstexit_is_abort', sa.Boolean(), nullable=True, comment='(TASK) Was the first exit from this task because it was aborted (1)?'),
    sa.Column('editing_time_s', sa.Float(), nullable=True, comment='(TASK) Time spent editing (s)'),
    sa.Column('_pk', sa.Integer(), autoincrement=True, nullable=False, comment='(SERVER) Primary key (on the server)'),
    sa.Column('_device_id', sa.Integer(), nullable=False, comment='(SERVER) ID of the source tablet device'),
    sa.Column('_era', sa.String(length=32), nullable=False, comment="(SERVER) 'NOW', or when this row was preserved and removed from the source device (UTC ISO 8601)"),
    sa.Column('_current', sa.Boolean(), nullable=False, comment='(SERVER) Is the row current (1) or not (0)?'),
    sa.Column('_when_added_exact', camcops_server.cc_modules.cc_sqla_coltypes.PendulumDateTimeAsIsoTextColType(length=32), nullable=True, comment='(SERVER) Date/time this row was added (ISO 8601)'),
    sa.Column('_when_added_batch_utc', sa.DateTime(), nullable=True, comment='(SERVER) Date/time of the upload batch that added this row (DATETIME in UTC)'),
    sa.Column('_adding_user_id', sa.Integer(), nullable=True, comment='(SERVER) ID of user that added this row'),
    sa.Column('_when_removed_exact', camcops_server.cc_modules.cc_sqla_coltypes.PendulumDateTimeAsIsoTextColType(length=32), nullable=True, comment='(SERVER) Date/time this row was removed, i.e. made not current (ISO 8601)'),
    sa.Column('_when_removed_batch_utc', sa.DateTime(), nullable=True, comment='(SERVER) Date/time of the upload batch that removed this row (DATETIME in UTC)'),
    sa.Column('_removing_user_id', sa.Integer(), nullable=True, comment='(SERVER) ID of user that removed this row'),
    sa.Column('_preserving_user_id', sa.Integer(), nullable=True, comment='(SERVER) ID of user that preserved this row'),
    sa.Column('_forcibly_preserved', sa.Boolean(), nullable=True, comment='(SERVER) Forcibly preserved by superuser (rather than normally preserved by tablet)?'),
    sa.Column('_predecessor_pk', sa.Integer(), nullable=True, comment='(SERVER) PK of predecessor record, prior to modification'),
    sa.Column('_successor_pk', sa.Integer(), nullable=True, comment='(SERVER) PK of successor record  (after modification) or NULL (whilst live, or after deletion)'),
    sa.Column('_manually_erased', sa.Boolean(), nullable=True, comment='(SERVER) Record manually erased (content destroyed)?'),
    sa.Column('_manually_erased_at', camcops_server.cc_modules.cc_sqla_coltypes.PendulumDateTimeAsIsoTextColType(length=32), nullable=True, comment='(SERVER) Date/time of manual erasure (ISO 8601)'),
    sa.Column('_manually_erasing_user_id', sa.Integer(), nullable=True, comment='(SERVER) ID of user that erased this row manually'),
    sa.Column('_camcops_version', camcops_server.cc_modules.cc_sqla_coltypes.SemanticVersionColType(length=147), nullable=True, comment='(SERVER) CamCOPS version number of the uploading device'),
    sa.Column('_addition_pending', sa.Boolean(), nullable=False, comment='(SERVER) Addition pending?'),
    sa.Column('_removal_pending', sa.Boolean(), nullable=True, comment='(SERVER) Removal pending?'),
    sa.Column('_group_id', sa.Integer(), nullable=False, comment='(SERVER) ID of group to which this record belongs'),
    sa.Column('id', sa.Integer(), nullable=False, comment='(TASK) Primary key (task ID) on the tablet device'),
    sa.Column('when_last_modified', camcops_server.cc_modules.cc_sqla_coltypes.PendulumDateTimeAsIsoTextColType(length=32), nullable=True, comment='(STANDARD) Date/time this row was last modified on the source tablet device (ISO 8601)'),
    sa.Column('_move_off_tablet', sa.Boolean(), nullable=True, comment='(SERVER/TABLET) Record-specific preservation pending?'),
    sa.ForeignKeyConstraint(['_adding_user_id'], ['_security_users.id'], name=op.f('fk_asdas__adding_user_id')),
    sa.ForeignKeyConstraint(['_device_id'], ['_security_devices.id'], name=op.f('fk_asdas__device_id')),
    sa.ForeignKeyConstraint(['_group_id'], ['_security_groups.id'], name=op.f('fk_asdas__group_id')),
    sa.ForeignKeyConstraint(['_manually_erasing_user_id'], ['_security_users.id'], name=op.f('fk_asdas__manually_erasing_user_id')),
    sa.ForeignKeyConstraint(['_preserving_user_id'], ['_security_users.id'], name=op.f('fk_asdas__preserving_user_id')),
    sa.ForeignKeyConstraint(['_removing_user_id'], ['_security_users.id'], name=op.f('fk_asdas__removing_user_id')),
    sa.PrimaryKeyConstraint('_pk', name=op.f('pk_asdas')),
    mysql_charset='utf8mb4 COLLATE utf8mb4_unicode_ci',
    mysql_engine='InnoDB',
    mysql_row_format='DYNAMIC'
    )
    with op.batch_alter_table('asdas', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_asdas__current'), ['_current'], unique=False)
        batch_op.create_index(batch_op.f('ix_asdas__device_id'), ['_device_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_asdas__era'), ['_era'], unique=False)
        batch_op.create_index(batch_op.f('ix_asdas__group_id'), ['_group_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_asdas__pk'), ['_pk'], unique=False)
        batch_op.create_index(batch_op.f('ix_asdas_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_asdas_patient_id'), ['patient_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_asdas_when_last_modified'), ['when_last_modified'], unique=False)

    # ### end Alembic commands ###


# noinspection PyPep8,PyTypeChecker
def downgrade():
    op.drop_table('asdas')
    # ### end Alembic commands ###
