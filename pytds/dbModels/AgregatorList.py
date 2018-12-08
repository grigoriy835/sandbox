from .Base import Base, MetaModel


class AgregatorList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'agregators'
