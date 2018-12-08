from .Base import Base, MetaModel


class OSVersionList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'os_version_list'
