from .Base import Base, MetaModel


class AgregatorRequestError(Base, metaclass=MetaModel):
    class Meta:
        db_table = 'agregator_request_error'
