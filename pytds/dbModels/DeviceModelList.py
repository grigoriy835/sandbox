from .Base import Base, MetaModel


class DeviceModelList(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'device_model_list'
