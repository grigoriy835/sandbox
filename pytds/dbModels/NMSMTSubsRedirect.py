from .Base import Base, MetaModel


class NMSMTSubsRedirect(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'nms_mt_subs_redirect'
