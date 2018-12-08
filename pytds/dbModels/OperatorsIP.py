from .Base import Base, MetaModel


class OperatorsIP(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'operators_ip'
