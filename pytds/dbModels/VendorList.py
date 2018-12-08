from .Base import Base, MetaModel


class VendorList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'vendor_list'
