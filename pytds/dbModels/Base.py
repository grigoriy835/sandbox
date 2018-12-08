from peewee import *
from peewee import BaseModel
from config import mysqlConfig
from playhouse.pool import PooledMySQLDatabase
import os

if os.environ.get('RUN_MOD') == 'TEST':
    config = mysqlConfig['test']
else:
    config = mysqlConfig['main']

db = PooledMySQLDatabase(**config['connection'])


def create_field(type='integer', pk=False):
    if type == 'varchar':
        return CharField(primary_key=pk)
    elif type == 'char':
        return FixedCharField(primary_key=pk)
    elif type == 'longtext' or type == 'text':
        return TextField(primary_key=pk)
    elif type == 'datetime':
        return DateTimeField(primary_key=pk)
    elif type == 'integer' or type == 'int' or type == 'tinyint':
        return IntegerField(primary_key=pk)
    elif type == 'bool':
        return BooleanField(primary_key=pk)
    elif type == 'real':
        return FloatField(primary_key=pk)
    elif type == 'double precision':
        return DoubleField(primary_key=pk)
    elif type == 'bigint':
        return BigIntegerField(primary_key=pk)
    elif type == 'smallint':
        return SmallIntegerField(primary_key=pk)
    elif type == 'numeric':
        return DecimalField(primary_key=pk)
    elif type == 'enum':
        return TextField(primary_key=pk)
    elif type == 'date':
        return DateField(primary_key=pk)
    elif type == 'time':
        return TimeField(primary_key=pk)
    elif type == 'blob':
        return BlobField(primary_key=pk)
    elif type == 'timestamp':
        return CharField(primary_key=pk)

    return None


class MetaModel(BaseModel):
    def __new__(cls, name, bases, attrs):
        if 'Meta' in attrs:
            meta = attrs['Meta']
            if meta:
                pks = []
                columns = db.get_columns(meta.db_table)
                for column in columns:
                    if column.primary_key:
                        pks.append(column)
                    else:
                        attrs[column.name] = create_field(column.data_type)

                if len(pks) > 1:
                    key_names = []
                    for column in pks:
                        key_names.append(column.name)
                        attrs[column.name] = create_field(column.data_type)
                    setattr(meta, 'primary_key', CompositeKey(*key_names))
                elif len(pks) == 1:
                    column = pks.pop()
                    if column.data_type in ['integer', 'int', 'tinyint']:
                        attrs[column.name] = PrimaryKeyField()
                    else:
                        attrs[column.name] = create_field(column.data_type, True)

        obj = super(MetaModel, cls).__new__(cls, name, bases, attrs)
        return obj


class Base(Model):
    def toDict(self):
        return self._data.copy()

    class Meta:
        database = db
        primary_key = False
