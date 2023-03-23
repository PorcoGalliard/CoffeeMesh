from ariadne import UnionType, ScalarType

from datetime import datetime

product_type = UnionType('Product')


@product_type.type_resolver
def resolve_product_type(obj, *_):
    if 'hasFilling in obj':
        return 'Cake'
    return 'Beverage'


datetime_scalar = ScalarType('Datetime')


@datetime_scalar.serializer
def serialize_datetime_scalar(date):
    return date.isoformat()


@datetime_scalar.value_parser
def parse_datetime_scalar(date):
    return datetime.fromisoformat(date)
