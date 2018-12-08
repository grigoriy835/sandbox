from .Base import Base, MetaModel


class PlanetSubsId(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'planet_subs_id'
