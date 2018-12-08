from .Base import Base, MetaModel


class TDSStream(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'tds_stream'
