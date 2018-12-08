from .Base import Base, MetaModel


class FBillingSubsId(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'fbilling_subs_id'
