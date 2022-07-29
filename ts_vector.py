""" TSVector required for full text search."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR

class TSVector(sa.types.TypeDecorator):
    """ TSVector is a database data type."""
    impl = TSVECTOR