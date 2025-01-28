# Mecha Custom Components
[![GitHub Actions](https://github.com/TheNuclearNexus/mecha-custom-components/workflows/CI/badge.svg)](https://github.com/TheNuclearNexus/mecha-custom-components/actions)
[![PyPI](https://img.shields.io/pypi/v/mecha-custom-components.svg)](https://pypi.org/project/mecha-custom-components/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mecha-custom-components.svg)](https://pypi.org/project/mecha-custom-components/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

> A library to easily extend your Mecha/Bolt code with custom components

## Introduction

This package provides an easy way to create your own custom components for mcfunction, using the Beet/Mecha ecosystem.

### Features
- Extensible component registry

## Example Usage
Extracted from [here](https://github.com/TheNuclearNexus/mecha-custom-components/tree/main/examples/basic_component_with_properties)

> [Beet](https://github.com/mcbeet/beet) Plugin
```py
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
```
> [Bolt](https://github.com/mcbeet/bolt) code
```mcfunction
give @s stick[example:foo={value: 1}]
```
When compiled becomes:
```mcfunction
give @s stick[minecraft:custom_data={foo: 1}]
```

More examples can be found in the [examples](https://github.com/TheNuclearNexus/mecha-custom-components/tree/main/examples) folder.

## Installation

The package can be installed with `pip`.
```
$ pip install mecha-custom-components
```