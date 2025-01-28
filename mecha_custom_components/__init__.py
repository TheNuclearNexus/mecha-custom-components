from dataclasses import InitVar, dataclass, replace
from functools import partial
from typing import Callable, Optional
from beet import Context
from nbtlib import Compound, Base, Byte
from beet.core.utils import extra_field, required_field
from mecha import (
    AstItemComponent,
    AstItemRemovedDefaultComponent,
    AstItemStack,
    AstNbt,
    AstResourceLocation,
    Mecha,
    MutatingReducer,
    rule,
)

ComponentTransformer = Callable[[Base, dict[str, Base]], dict[str, Base]]


def components_to_ast(components: dict[str, Base]):
    arguments = []

    for key, value in components.items():
        if key.startswith("!"):
            key_node = AstResourceLocation.from_value(key[1:])
            arguments.append(AstItemRemovedDefaultComponent(key=key_node))
        else:
            key_node = AstResourceLocation.from_value(key)
            arguments.append(
                AstItemComponent(key=key_node, value=AstNbt.from_value(value))
            )

    return arguments


@dataclass
class ComponentCollector(MutatingReducer):
    registry: "CustomComponentRegistry" = required_field()

    @rule(AstItemStack)
    def item_stack(self, node: AstItemStack):
        components: dict[str, Base] = {}
        transformers: list[ComponentTransformer] = []
        for component in node.arguments:
            key = component.key.get_canonical_value()
            if isinstance(component, AstItemRemovedDefaultComponent):
                components[f"!{key}"] = Compound({})
            elif transformer := self.registry.get(key):
                transformers.append(partial(transformer, component.value.evaluate()))
            else:
                components[key] = component.value.evaluate()

        if len(transformers) == 0:
            return node

        for transformer in transformers:
            components = transformer(components)

        return replace(node, arguments=components_to_ast(components))


@dataclass
class CustomComponentRegistry:
    ctx: InitVar[Optional[Context]] = None

    collector: ComponentCollector = extra_field(default=None)
    custom_components: dict[str, ComponentTransformer] = extra_field(
        default_factory=dict
    )

    def __post_init__(self, ctx: Optional[Context]):
        self.collector = ComponentCollector(registry=self)

        if ctx is not None:
            mecha = ctx.inject(Mecha)
            mecha.transform.extend(self.collector)

    def extend(self, key: str, component: ComponentTransformer):
        parts = key.lower().split(":")
        if len(parts) == 1:
            key = "minecraft:" + parts[0]

        if key in self.custom_components:
            raise Exception(f"Component '{key}' has already been registered")

        self.custom_components[key] = component

    def has(self, key: str):
        return key in self.custom_components

    def get(self, key: str) -> ComponentTransformer | None:
        return self.custom_components.get(key)
