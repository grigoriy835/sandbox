from .Base import Base, MetaModel


class TDSLand(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'tds_land'
