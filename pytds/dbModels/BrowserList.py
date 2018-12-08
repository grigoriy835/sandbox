from .Base import Base, MetaModel


class BrowserList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'browser_list'
