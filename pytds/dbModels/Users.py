from .Base import Base, MetaModel


class Users(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'users'
