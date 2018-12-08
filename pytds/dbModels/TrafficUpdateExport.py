from .Base import Base, MetaModel


class TrafficUpdateExport(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'tds_traffic_update_export'

