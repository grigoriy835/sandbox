from .Base import Base, MetaModel


class OSList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'os_list'
