# Lectern snapshot

## Data pack

`@data_pack pack.mcmeta`

```json
{
  "pack": {
    "pack_format": 61,
    "description": ""
  }
}
```

### event

`@advancement event:on_click`

```json
{
  "criteria": {
    "using": {
      "trigger": "minecraft:using_item",
      "conditions": {
        "item": {
          "components": {
            "minecraft:custom_data": {
              "event": {
                "on_click": {}
              }
            }
          }
        }
      }
    }
  },
  "rewards": {
    "function": "event:on_click"
  }
}
```

`@function event:on_click`

```mcfunction
advancement revoke @s only event:on_click
function event:on_click/run with entity @s SelectedItem.components."minecraft:custom_data".event
```

`@function event:on_click/run`

```mcfunction
$function $(on_click)
```

### test

`@function test:foo`

```mcfunction
give @s stick[minecraft:custom_data={event: {on_click: "test:click"}}, minecraft:consumable={consume_seconds: 2147483647, animation: "block"}, !minecraft:food]
give @s stick[minecraft:custom_data={event: {on_click: "test:click"}}, minecraft:consumable={consume_seconds: 2147483647, animation: "block"}, !minecraft:food]
give @s stick[minecraft:custom_data={event: {on_click: "test:click"}}, minecraft:consumable={consume_seconds: 2147483647, animation: "eat"}, !minecraft:food]
```

`@function test:click`

```mcfunction
say clicked!
```
