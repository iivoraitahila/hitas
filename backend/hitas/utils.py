import datetime
import operator
from typing import Any, Optional

from django.db.models import Value
from django.db.models.functions import Round
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication


class RoundWithPrecision(Round):
    """Implement round from Django 4.0
    https://github.com/django/django/blob/main/django/db/models/functions/math.py#L176
    """

    arity = None  # Override Transform's arity=1 to enable passing precision.

    def __init__(self, expression, precision=0, **extra):
        super().__init__(expression, precision, **extra)

    def as_sqlite(self, compiler, connection, **extra_context):
        precision = self.get_source_expressions()[1]
        if isinstance(precision, Value) and precision.value < 0:
            raise ValueError("SQLite does not support negative precision.")
        return super().as_sqlite(compiler, connection, **extra_context)

    def _resolve_output_field(self):
        source = self.get_source_expressions()[0]
        return source.output_field


def safe_attrgetter(obj: Any, dotted_path: str, default: Optional[Any]) -> Any:
    """
    Examples:
        >>> safe_attrgetter(object, "__class__.__name__.__class__.__name__")
        'str'
        >>> safe_attrgetter(object, "foo.bar.baz") is None
        True
        >>> safe_attrgetter(object, "foo.bar.baz", default="")
        ''
    """
    try:
        return operator.attrgetter(dotted_path)(obj)
    except AttributeError:
        return default


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"


def this_month() -> datetime.date:
    return monthify(timezone.now().today().date())


def monthify(date: datetime.date) -> datetime.date:
    return date.replace(day=1)
