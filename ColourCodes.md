# Colour Codes

Clean reference for the core UI palette.

> If your Markdown preview supports inline HTML, swatches will render in the **Preview** column.
> The palette below is for creating/editing your button and UI texture assets.

| Name | Hex | Preview | Usage |
|---|---|---|---|
| Gold Border Start | `#FFD700` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#FFD700;"></span> | Border gradient (start) |
| Gold Border End | `#FFAA00` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#FFAA00;"></span> | Border gradient (end) |
| Purple Idle | `#704A9F` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#704A9F;"></span> | Main idle button color |
| Purple Hover | `#361B58` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#361B58;"></span> | Main hover button color |
| Pink Fill Idle | `#F20DAF` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#F20DAF;"></span> | Fill/accent idle |
| Pink Fill Hover | `#85045F` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#85045F;"></span> | Fill/accent hover |

## Other In-Game Colors

These are other colors currently used in screens/components.

| Name | Hex | Preview | Usage |
|---|---|---|---|
| White Text | `#FFFFFF` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#FFFFFF;"></span> | Main button/label text |
| Primary Purple Border | `#6B3AA8` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#6B3AA8;"></span> | Panel borders / strong outlines |
| Secondary Purple Outline | `#5A3192` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#5A3192;"></span> | Secondary text outline |
| Deep Purple Outline | `#47286F` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#47286F;"></span> | Body text outline |
| Orange Accent | `#FF8335` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#FF8335;"></span> | Hover/accent states |
| Panel Overlay | `#120D20BB` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#120D20BB;"></span> | Menu background tint |
| Modal Dim | `#0008` | <span style="display:inline-block;width:72px;height:16px;border:1px solid #999;background:#0008;"></span> | Modal dim overlay |

## Copy/Paste List

```txt
#FFD700
#FFAA00
#704A9F
#361B58
#F20DAF
#85045F
```

## Ren'Py Example

```renpy
style my_button_text:
    color "#FFFFFF"
    outlines [(3, "#361B58", 0, 0)]

add Solid("#704A9F")
```
