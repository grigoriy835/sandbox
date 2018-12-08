from .Base import Base, MetaModel


class IceSubIdTables(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'ice_sub_id_tables'
