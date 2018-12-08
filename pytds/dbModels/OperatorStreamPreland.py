from .Base import Base, MetaModel


class OperatorStreamPreland(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'operator_stream_preland'
