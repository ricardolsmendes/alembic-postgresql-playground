import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.ext import declarative
from sqlalchemy.sql import ddl


Base = declarative.declarative_base()


class PartitionedTableMixin:
    city_id = sa.Column(sa.Integer, primary_key=True)
    log_date = sa.Column(sa.Date, primary_key=True)
    peaktemp = sa.Column(sa.Integer)
    unitsales = sa.Column(sa.Integer)


class PartitionedTable(PartitionedTableMixin, Base):
    __tablename__ = "partitioned_table"
    __table_args__ = {"postgresql_partition_by": "RANGE (log_date)"}


class PartitionedTable2023(PartitionedTableMixin, Base):
    __tablename__ = "partitioned_table_2023"


PartitionedTable2023.__table__.add_is_dependent_on(PartitionedTable.__table__)

event.listen(
    PartitionedTable2023.__table__,
    "after_create",
    ddl.DDL(
        """
        ALTER TABLE partitioned_table
        ATTACH PARTITION partitioned_table_2023
        FOR VALUES FROM ('2023-01-01 00:00:00') TO ('2023-01-01 00:00:00');
        """
    ),
)
