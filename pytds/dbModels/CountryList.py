from .Base import Base, MetaModel


class CountryList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'country_list'
