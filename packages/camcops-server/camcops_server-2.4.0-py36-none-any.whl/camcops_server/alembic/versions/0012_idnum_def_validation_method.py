#!/usr/bin/env python

"""
camcops_server/alembic/versions/0012_idnum_def_validation_method.py

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

_idnum_definitions.validation_method

Revision ID: 0012
Revises: 0011
Creation date: 2018-11-05 13:16:39.101358

"""

# =============================================================================
# Imports
# =============================================================================

from alembic import op
import sqlalchemy as sa


# =============================================================================
# Revision identifiers, used by Alembic.
# =============================================================================

revision = '0012'
down_revision = '0011'
branch_labels = None
depends_on = None


# =============================================================================
# The upgrade/downgrade steps
# =============================================================================

# noinspection PyPep8,PyTypeChecker
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('_idnum_definitions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('validation_method', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


# noinspection PyPep8,PyTypeChecker
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('_idnum_definitions', schema=None) as batch_op:
        batch_op.drop_column('validation_method')

    # ### end Alembic commands ###
