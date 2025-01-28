from beet import Context
from nbtlib import Compound, Base, Byte

from mecha_custom_components import CustomComponentRegistry


def test_transformer(properties: Base, components: dict[str, Base]):
    custom_data = components.setdefault("minecraft:custom_data", Compound({}))

    if not isinstance(custom_data, Compound):
        raise Exception("Existing custom data is not a compound!")

    custom_data.merge({"test": Byte(1)})

    return components


def beet_default(ctx: Context):
    registry = ctx.inject(CustomComponentRegistry)

    registry.extend("test", test_transformer)
