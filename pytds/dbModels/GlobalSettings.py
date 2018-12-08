from .Base import Base, MetaModel


class GlobalSettings(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'global_settings'
