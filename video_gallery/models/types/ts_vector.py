import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR


# noinspection PyAbstractClass
class TSVector(sa.types.TypeDecorator):  # pylint:disable=abstract-method
    impl = TSVECTOR
