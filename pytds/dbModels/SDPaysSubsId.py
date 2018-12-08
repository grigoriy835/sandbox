from .Base import Base, MetaModel


class SDPaysSubsId(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'sd_pays_subs_id'