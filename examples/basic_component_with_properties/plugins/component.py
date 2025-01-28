from beet import Context
from nbtlib import Compound, Base

from beet import Context
from nbtlib import Base, Compound
from mecha_custom_components import CustomComponentRegistry


def simple_component(properties: Base, components: dict[str, Base]):
    if not isinstance(properties, Compound):
        raise Exception("'example:simple' expects a compound!")

    custom_data = components.setdefault("minecraft:custom_data", Compound({}))

    if not isinstance(custom_data, Compound):
        raise Exception("Existing custom_data was not a compound!")

    custom_data.merge({"foo": properties["value"]})

    return components


def beet_default(ctx: Context):
    registry = ctx.inject(CustomComponentRegistry)
    registry.extend("example:foo", simple_component)
