from ariadne import UnionType, ScalarType, InterfaceType, ObjectType
import copy

from datetime import datetime

from web.data import ingredients, products

product_type = UnionType('Product')
product_interface = InterfaceType('ProductInterface')


@product_interface.field('ingredients')
def resolve_product_ingredients(product, _):
    recipe = [
        copy.copy(ingredient)
        for ingredient in product.get("ingredients", [])
    ]

    for ingredient_recipe in recipe:
        for ingredient in ingredients:
            if ingredient['id'] == ingredient_recipe['ingredient']:
                ingredient_recipe['ingredient'] = ingredient

    return recipe


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
