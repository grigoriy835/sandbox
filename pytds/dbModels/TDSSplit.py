from .Base import Base, MetaModel


class TDSSplit(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'tds_split'
