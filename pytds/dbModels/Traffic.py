from .Base import Base, MetaModel
from .TrafficUpdateExport import TrafficUpdateExport


class Traffic(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'tds_traffic'

    # как ни печально но я ничего особо не придумал чтобы было по нормальному
    # этот метод надо вызывать перед внесением изменений в модель и сохранением в базу
    # чтобы это изменение учитывалось в статистике
    def before_update_record(self):
        data = self.toDict()
        data['sign'] = -1
        data.pop('subs')
        data.pop('cookie_set_datetime')
        data.pop('user_agent')
        data.pop('cookie_value')
        data.pop('location')
        data.pop('ref_full')
        TrafficUpdateExport.insert(**data).execute()
