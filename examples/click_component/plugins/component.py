from typing import cast
from beet import Advancement, Context, Function
from nbtlib import Compound, Base, String

from beet import Context
from nbtlib import Base, Compound
from mecha_custom_components import CustomComponentRegistry

CLICK_ADVANCEMENT = Advancement({
    "criteria": {
        "using": {
            "trigger": "minecraft:using_item",
            "conditions": {
                "item": {
                    "components": {"minecraft:custom_data": {"event": {"on_click": {}}}}
                }
            },
        }
    },
    "rewards": {"function": "event:on_click"},
})

CLICK_FUNCTION = Function("""
advancement revoke @s only event:on_click
function event:on_click/run with entity @s SelectedItem.components."minecraft:custom_data".event
""")

CLICK_RUN_FUNCTION = Function("""
$function $(on_click)
""")


def on_click_component(properties: Base, components: dict[str, Base]):
    if not (isinstance(properties, Compound) or isinstance(properties, String)):
        raise Exception(
            f"'event:on_click' expects a compound or string! Received: {type(properties)}"
        )

    if isinstance(properties, String):
        properties = Compound({"function": properties, "animation": "block"})

    properties.setdefault("animation", "block")

    custom_data = components.setdefault("minecraft:custom_data", Compound({}))

    if not isinstance(custom_data, Compound):
        raise Exception("Existing custom_data was not a compound!")

    components["minecraft:consumable"] = Compound(
        {"consume_seconds": (2**31) - 1, "animation": properties["animation"]}
    )

    components["!minecraft:food"] = Compound({})

    custom_data.merge({"event": {"on_click": properties["function"]}})

    return components


def beet_default(ctx: Context):
    registry = ctx.inject(CustomComponentRegistry)
    registry.extend("event:on_click", on_click_component)

    ctx.generate("event:on_click", CLICK_ADVANCEMENT)
    ctx.generate("event:on_click", CLICK_FUNCTION)
    ctx.generate("event:on_click/run", CLICK_RUN_FUNCTION)
