from .Base import Base, MetaModel


class BadReferersList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'bad_referers_lists'
