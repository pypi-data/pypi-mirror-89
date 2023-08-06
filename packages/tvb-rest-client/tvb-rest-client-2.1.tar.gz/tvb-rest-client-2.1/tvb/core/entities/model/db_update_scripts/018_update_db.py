# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
# Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
# Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Change of DB structure to TVB 2.0

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
.. moduleauthor:: Robert Vincze <robert.vincze@codemart.ro>
"""
import json
import uuid
from migrate import create_column, drop_column, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy import Column, String, Integer
from tvb.basic.logger.builder import get_logger
from tvb.core.entities.storage import SA_SESSIONMAKER
from sqlalchemy.sql import text
from tvb.core.neotraits.db import Base

meta = Base.metadata
LOGGER = get_logger(__name__)


BURST_COLUMNS = [Column('range1', String), Column('range2', String), Column('fk_simulation', Integer),
Column('fk_operation_group', Integer), Column('fk_metric_operation_group', Integer)]
BURST_DELETED_COLUMN = Column('workflows_number', Integer)

OP_COLUMN = Column('view_model_disk_size', Integer)
OP_DELETED_COLUMN = Column('meta_data', String)

USER_COLUMNS = [Column('gid', String), Column('display_name', String)]


def migrate_range_params(ranges):
    new_ranges = []
    for range in ranges:
        list_range = eval(range)

        if list_range is None:
            new_ranges.append('None')
            continue

        # in the range param name if the range param is not a gid param then
        # all the characters between the first and last underscores (including them)
        # must be deleted and replaced with a dot

        param_name = list_range[0]
        param_range = list_range[1]
        if '_' in param_name:
            if param_name.count('_') > 1:
                first_us = param_name.index('_')
                last_us = param_name.rfind('_')
                string_to_be_replaced = param_name[first_us:last_us + 1]
                param_name = param_name.replace(string_to_be_replaced, '.')

            param_name = "\"" + param_name  + "\""

            # in the old version the range was a list of all values that the param had, but in the new one we
            # need only the minimum, maximum and step value
            range_dict = dict()
            range_dict['\"lo\"'] = param_range[0]
            range_dict['\"hi\"'] = param_range[-1]
            range_dict['\"step\"'] = param_range[1] - param_range[0]
            new_ranges.append([param_name, range_dict])
        else:
            # We have a gid param
            new_ranges.append(['\"' + param_name + '\"', 'null'])
    return new_ranges


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    session = SA_SESSIONMAKER()

    try:
        session.execute(text("""ALTER TABLE "BURST_CONFIGURATIONS"
                                        RENAME TO "BurstConfiguration"; """))

        # Dropping tables which don't exist in the new version
        session.execute(text("""DROP TABLE "MAPPED_LOOK_UP_TABLE_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_DATATYPE_MEASURE_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_SPATIAL_PATTERN_VOLUME_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_SIMULATION_STATE_DATA";"""))
        session.execute(text("""DROP TABLE "WORKFLOW_STEPS";"""))
        session.execute(text("""DROP TABLE "WORKFLOW_VIEW_STEPS";"""))

        # Dropping tables which will be repopulated from the H5 files
        session.execute(text("""DROP TABLE "MAPPED_COHERENCE_SPECTRUM_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_COMPLEX_COHERENCE_SPECTRUM_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_CONNECTIVITY_ANNOTATIONS_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_CONNECTIVITY_MEASURE_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_CONNECTIVITY_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_CORRELATION_COEFFICIENTS_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_COVARIANCE_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_CROSS_CORRELATION_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_FCD_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_FOURIER_SPECTRUM_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_INDEPENDENT_COMPONENTS_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_LOCAL_CONNECTIVITY_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_PRINCIPAL_COMPONENTS_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_PROJECTION_MATRIX_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_REGION_MAPPING_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_REGION_VOLUME_MAPPING_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_TIME_SERIES_REGION_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_TIME_SERIES_EEG_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_TIME_SERIES_MEG_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_TIME_SERIES_SEEG_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_TIME_SERIES_SURFACE_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_TIME_SERIES_VOLUME_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_SENSORS_DATA" """))
        session.execute(text("""DROP TABLE "MAPPED_TRACTS_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_STIMULI_REGION_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_STIMULI_SURFACE_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_STRUCTURAL_MRI_DATA" """))
        session.execute(text("""DROP TABLE "MAPPED_SURFACE_DATA" """))
        session.execute(text("""DROP TABLE "MAPPED_VALUE_WRAPPER_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_VOLUME_DATA" """))
        session.execute(text("""DROP TABLE "MAPPED_WAVELET_COEFFICIENTS_DATA";"""))
        session.execute(text("""DROP TABLE "DATA_TYPES_GROUPS";"""))
        session.execute(text("""DROP TABLE "MAPPED_ARRAY_DATA";"""))
        session.execute(text("""DROP TABLE "MAPPED_SPATIO_TEMPORAL_PATTERN_DATA" """))
        session.execute(text("""DROP TABLE "MAPPED_SPATIAL_PATTERN_DATA";"""))
        session.execute(text("""DROP TABLE "WORKFLOWS";"""))
        session.execute(text("""DROP TABLE "MAPPED_TIME_SERIES_DATA";"""))
        session.commit()
    except Exception as excep:
        LOGGER.exception(excep)
    finally:
        session.close()

    # MIGRATING USERS #
    users_table = meta.tables['USERS']
    for column in USER_COLUMNS:
        create_column(column, users_table)

    session = SA_SESSIONMAKER()
    try:
        user_ids = eval(str(session.execute(text("""SELECT U.id
                            FROM "USERS" U """)).fetchall()))

        for id in user_ids:
            session.execute(text("""UPDATE "USERS" SET display_name = username,
                gid ='""" + uuid.uuid4().hex + """' WHERE id = """ + str(id[0])))
        session.commit()
    except Exception as excep:
        LOGGER.exception(excep)
    finally:
        session.close()

    UniqueConstraint("gid", table=users_table)

    # Migrating BurstConfiguration
    burst_config_table = meta.tables['BurstConfiguration']
    for column in BURST_COLUMNS:
        create_column(column, burst_config_table)

    session = SA_SESSIONMAKER()
    try:
        session.execute(text("""ALTER TABLE "BurstConfiguration"
                                RENAME COLUMN _dynamic_ids TO dynamic_ids"""))
        session.execute(text("""ALTER TABLE "BurstConfiguration"
                                RENAME COLUMN _simulator_configuration TO simulator_gid"""))

        ranges = session.execute(text("""SELECT OG.id, OG.range1, OG.range2
                            FROM "OPERATION_GROUPS" OG""")).fetchall()
        session.execute(text(
            """DELETE FROM "BurstConfiguration" WHERE status = \'error\'"""))

        ranges_1 = []
        ranges_2 = []

        for r in ranges:
            ranges_1.append(str(r[1]))
            ranges_2.append(str(r[2]))

        new_ranges_1 = migrate_range_params(ranges_1)
        new_ranges_2 = migrate_range_params(ranges_2)
        operation_groups = session.execute(text("""SELECT * FROM "OPERATION_GROUPS" """)).fetchall()

        for op_g in operation_groups:
            op = eval(str(session.execute(text("""SELECT fk_operation_group, parameters, meta_data 
            FROM "OPERATIONS" O WHERE O.fk_operation_group = """ + str(op_g[0]))).fetchone()))
            burst_id = eval(op[2])['Burst_Reference']

            if 'time_series' in op[1]:
                session.execute(
                    text("""UPDATE "BurstConfiguration" as B SET fk_metric_operation_group = """ + str(op[0]) +
                         """ WHERE B.id = """ + str(burst_id)))
            else:
                session.execute(
                    text("""UPDATE "BurstConfiguration" as B SET fk_operation_group = """ + str(op[0]) +
                         """ WHERE B.id = """ + str(burst_id)))

        for i in range(len(ranges_1)):
            range1 =  str(new_ranges_1[i]).replace('\'', '')
            range2 = str(new_ranges_2[i]).replace('\'', '')

            session.execute(text(
                """UPDATE "BurstConfiguration" SET
                range1 = '""" + range1 + """'
                WHERE fk_operation_group = """ + str(ranges[i][0])))

            session.execute(text(
                """UPDATE "OPERATION_GROUPS" SET
                range1 = '""" + range1 + """'
                WHERE id = """ + str(ranges[i][0])))

            if range2 != 'None':
                session.execute(text(
                    """UPDATE "BurstConfiguration" SET
                    range2 = '""" + range2 + """'
                    WHERE fk_operation_group = """ + str(ranges[i][0])))

                session.execute(text(
                    """UPDATE "OPERATION_GROUPS" SET
                    range2 = '""" + range2 + """'
                    WHERE id = """ + str(ranges[i][0])))

        session.commit()
    except Exception:
        session.close()
    finally:
        session.close()

    # Drop old column
    drop_column(BURST_DELETED_COLUMN, burst_config_table)

    # Create constraints only after the rows are populated
    fk_burst_config_constraint_1 = ForeignKeyConstraint(
        ["fk_simulation"],
        ["OPERATIONS.id"],
        table=burst_config_table)
    fk_burst_config_constraint_2 = ForeignKeyConstraint(
        ["fk_operation_group"],
        ["OPERATION_GROUPS.id"],
        table=burst_config_table)
    fk_burst_config_constraint_3 = ForeignKeyConstraint(
        ["fk_metric_operation_group"],
        ["OPERATION_GROUPS.id"],
        table=burst_config_table)

    fk_burst_config_constraint_1.create()
    fk_burst_config_constraint_2.create()
    fk_burst_config_constraint_3.create()

    # MIGRATING Operations #
    session = SA_SESSIONMAKER()
    try:
        burst_ref_metadata = session.execute(text("""SELECT id, meta_data FROM "OPERATIONS"
                    WHERE meta_data like '%Burst_Reference%' """)).fetchall()

        for metadata in burst_ref_metadata:
            metadata_dict = eval(str(metadata[1]))
            session.execute(text("""UPDATE "OPERATIONS" SET parameters = '""" +
                                 json.dumps(metadata_dict['Burst_Reference']) + """' WHERE id = """ + str(metadata[0])))

        session.execute(text("""ALTER TABLE "OPERATIONS"
                                    RENAME COLUMN parameters TO view_model_gid"""))

        # Name it back to the old name, because we have to keep both tables so we can create BurstConfigurationH5s
        session.execute(text("""ALTER TABLE "BurstConfiguration"
                                                RENAME TO "BURST_CONFIGURATION"; """))
        session.commit()
    except Exception as excep:
        LOGGER.exception(excep)
    finally:
        session.close()

    session = SA_SESSIONMAKER()
    try:
        session.execute(text("""DROP TABLE "ALGORITHMS"; """))
        session.execute(text("""DROP TABLE "ALGORITHM_CATEGORIES"; """))
        session.execute(text("""DROP TABLE "DATA_TYPES"; """))
        session.commit()
    except Exception as excep:
        # If the drops fail, it could mean we are using postgresql
        session.close()
        session = SA_SESSIONMAKER()
        LOGGER.exception(excep)
        try:
            session.execute(text("""DROP TABLE if exists "ALGORITHMS" cascade; """))
            session.execute(text("""DROP TABLE if exists "ALGORITHM_CATEGORIES" cascade; """))
            session.execute(text("""DROP TABLE if exists "DATA_TYPES" cascade; """))
            session.commit()
        except Exception as excep:
            LOGGER.exception(excep)
    finally:
        session.close()

    op_table = meta.tables['OPERATIONS']
    create_column(OP_COLUMN, op_table)
    drop_column(OP_DELETED_COLUMN, op_table)


def downgrade(_):
    """
    Downgrade currently not supported
    """
    pass
