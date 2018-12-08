from .Base import Base, MetaModel


class OperatorUserPreland(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'operator_user_preland'
