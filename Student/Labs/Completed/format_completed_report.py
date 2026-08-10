from __future__ import annotations

import hashlib
import json
from pathlib import Path
import secrets
import zipfile


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Completed_Report.pbix"
OUTPUT = ROOT / "Completed_Report_Professional.pbix"
LAYOUT_PATH = "Report/Layout"
THEME_PATH = "Report/StaticResources/SharedResources/BaseThemes/Fluent2-CY26SU08.json"

PAGE_LAYOUTS = {
    "Financial Health": [
        (64, 112, 420, 132),
        (508, 112, 420, 132),
        (952, 112, 420, 132),
        (1396, 112, 420, 132),
        (1552, 278, 264, 100),
        (1552, 398, 264, 100),
        (1552, 518, 264, 100),
        (64, 278, 720, 340),
        (808, 278, 720, 340),
        (64, 650, 1752, 366),
    ],
    "Procurement Exposure": [
        (64, 112, 850, 140),
        (64, 284, 700, 300),
        (788, 284, 600, 300),
        (1412, 284, 404, 300),
        (64, 616, 1752, 400),
        (938, 112, 280, 140),
        (1230, 112, 268, 140),
        (1510, 112, 306, 140),
    ],
    "Executive Review": [
        (64, 112, 1050, 150),
        (64, 294, 760, 722),
        (848, 294, 968, 722),
        (1138, 112, 330, 150),
        (1492, 112, 324, 150),
    ],
}

VISUAL_TITLES = {
    "Financial Health": {
        "clusteredBarChart": "Budget vs. Actual by Program",
        "lineChart": "Actual Spend Trend by Fiscal Period",
        "pivotTable": "Budget Variance by Program and Fiscal Period",
    },
    "Procurement Exposure": {
        "barChart": "Outstanding Commitment by Vendor",
        "clusteredColumnChart": "Purchase Order Value by Program",
        "donutChart": "Purchase Orders by Status",
        "tableEx": "Purchase Order Detail",
    },
    "Executive Review": {
        "barChart": "Budget Variance by Program",
        "pivotTable": "Executive Financial and Procurement Summary",
    },
}


def literal(value: str) -> dict:
    return {"expr": {"Literal": {"Value": value}}}


def set_position(container: dict, position: tuple[int, int, int, int]) -> None:
    x, y, width, height = position
    container.update(x=x, y=y, width=width, height=height)
    config = json.loads(container["config"])
    layout_position = config["layouts"][0]["position"]
    layout_position.update(x=x, y=y, width=width, height=height)
    container["config"] = json.dumps(config, separators=(",", ":"))


def set_visual_title(container: dict, title: str) -> None:
    config = json.loads(container["config"])
    single_visual = config["singleVisual"]
    title_objects = single_visual.setdefault("vcObjects", {}).setdefault("title", [])
    if not title_objects:
        title_objects.append({"properties": {}})
    properties = title_objects[0].setdefault("properties", {})
    properties["show"] = literal("true")
    properties["text"] = literal(f"'{title}'")
    container["config"] = json.dumps(config, separators=(",", ":"))


def add_page_header(section: dict) -> None:
    name = secrets.token_hex(10)
    z_index = max((visual.get("z", 0) for visual in section["visualContainers"]), default=0) + 1
    position = {"x": 64, "y": 22, "z": z_index, "width": 1000, "height": 64}
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": position.copy()}],
        "singleVisual": {
            "visualType": "textbox",
            "drillFilterOtherVisuals": True,
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": [
                                {
                                    "textRuns": [
                                        {
                                            "value": section["displayName"],
                                            "textStyle": {
                                                "fontWeight": "bold",
                                                "fontSize": "28pt",
                                                "fontFamily": "Segoe UI Semibold",
                                                "color": "#16324F",
                                            },
                                        }
                                    ],
                                    "horizontalTextAlignment": "left",
                                }
                            ]
                        }
                    }
                ]
            },
        },
    }
    section["visualContainers"].append(
        {
            **position,
            "config": json.dumps(config, separators=(",", ":")),
            "filters": "[]",
        }
    )


def style_page(section: dict) -> None:
    section["config"] = json.dumps(
        {
            "objects": {
                "background": [
                    {
                        "properties": {
                            "color": {"solid": {"color": literal("'#F4F6F8'")}},
                            "transparency": literal("0D"),
                        }
                    }
                ],
                "outspace": [
                    {
                        "properties": {
                            "color": {"solid": {"color": literal("'#E8EDF2'")}},
                            "transparency": literal("0D"),
                        }
                    }
                ],
            }
        },
        separators=(",", ":"),
    )


def format_layout(layout: dict) -> None:
    for section in layout["sections"]:
        page_name = section["displayName"]
        positions = PAGE_LAYOUTS[page_name]
        if len(section["visualContainers"]) != len(positions):
            raise ValueError(f"Unexpected visual count on {page_name}")
        title_counts: dict[str, int] = {}
        for container, position in zip(section["visualContainers"], positions):
            set_position(container, position)
            config = json.loads(container["config"])
            visual_type = config["singleVisual"]["visualType"]
            title = VISUAL_TITLES.get(page_name, {}).get(visual_type)
            if title:
                title_counts[visual_type] = title_counts.get(visual_type, 0) + 1
                set_visual_title(container, title)
        style_page(section)
        add_page_header(section)
    report_config = json.loads(layout["config"])
    report_config["activeSectionIndex"] = 0
    layout["config"] = json.dumps(report_config, separators=(",", ":"))


def format_theme(theme: dict) -> None:
    theme.update(
        name="Coding-Forge Finance Executive",
        dataColors=[
            "#16324F",
            "#2A7F8E",
            "#4C78A8",
            "#D6A84B",
            "#6B7C93",
            "#4F8A68",
            "#C75C5C",
            "#8C6BB1",
        ],
        background="#FFFFFF",
        foreground="#17212B",
        tableAccent="#16324F",
        good="#4F8A68",
        neutral="#D6A84B",
        bad="#C75C5C",
        maximum="#2A7F8E",
        center="#F4F6F8",
        minimum="#DCE6EF",
    )
    global_styles = theme["visualStyles"]["*"]["*"]
    global_styles["title"][0].update(
        show=True,
        fontSize=15,
        fontFamily="Segoe UI Semibold",
        fontColor={"solid": {"color": "#16324F"}},
    )
    global_styles["background"][0].update(
        show=True, transparency=0, color={"solid": {"color": "#FFFFFF"}}
    )
    global_styles["border"][0].update(
        show=True,
        width=1,
        radius=6,
        color={"solid": {"color": "#D8E0E7"}},
    )
    global_styles["dropShadow"][0]["show"] = False
    global_styles["categoryAxis"][0].update(
        gridlineColor={"solid": {"color": "#E7EBEF"}},
        labelColor={"solid": {"color": "#4B5563"}},
    )
    global_styles["valueAxis"][0].update(
        gridlineColor={"solid": {"color": "#E7EBEF"}},
        labelColor={"solid": {"color": "#4B5563"}},
    )
    page = theme["visualStyles"]["page"]["*"]
    page["background"][0].update(
        color={"solid": {"color": "#F4F6F8"}}, transparency=0
    )
    page["outspace"][0]["color"] = {"solid": {"color": "#E8EDF2"}}
    cards = theme["visualStyles"]["cardVisual"]["*"]
    cards["background"][0].update(
        show=True, transparency=0, color={"solid": {"color": "#FFFFFF"}}
    )
    cards["border"][0].update(
        show=True, color={"solid": {"color": "#D8E0E7"}}, radius=6
    )
    cards["label"][0].update(
        fontSize=11, fontColor={"solid": {"color": "#5B6573"}}
    )
    slicers = theme["visualStyles"]["slicer"]["*"]
    slicers["background"][0].update(
        show=True, transparency=0, color={"solid": {"color": "#FFFFFF"}}
    )
    slicers["border"][0].update(
        show=True, color={"solid": {"color": "#D8E0E7"}}, radius=6
    )
    for visual_type in ("tableEx", "pivotTable"):
        styles = theme["visualStyles"][visual_type]
        styles["None"]["columnHeaders"][0].update(
            fontColor={"solid": {"color": "#FFFFFF"}},
            backColor={"solid": {"color": "#16324F"}},
        )
        if "rowHeaders" in styles["None"]:
            styles["None"]["rowHeaders"][0].update(
                fontColor={"solid": {"color": "#17212B"}},
                backColor={"solid": {"color": "#F4F6F8"}},
            )
        styles["None"]["values"][0].update(
            backColorPrimary={"solid": {"color": "#FFFFFF"}},
            backColorSecondary={"solid": {"color": "#F7F9FB"}},
        )


def build() -> None:
    with zipfile.ZipFile(SOURCE, "r") as source_zip:
        layout = json.loads(source_zip.read(LAYOUT_PATH).decode("utf-16-le"))
        theme = json.loads(source_zip.read(THEME_PATH).decode("utf-8-sig"))
        source_model_hash = hashlib.sha256(source_zip.read("DataModel")).hexdigest()
        format_layout(layout)
        format_theme(theme)
        replacements = {
            LAYOUT_PATH: json.dumps(layout, separators=(",", ":")).encode("utf-16-le"),
            THEME_PATH: json.dumps(theme, separators=(",", ":")).encode("utf-8"),
        }
        with zipfile.ZipFile(OUTPUT, "w") as output_zip:
            for entry in source_zip.infolist():
                if entry.filename == "SecurityBindings":
                    continue
                output_zip.writestr(entry, replacements.get(entry.filename, source_zip.read(entry.filename)))

    with zipfile.ZipFile(OUTPUT, "r") as output_zip:
        validated_layout = json.loads(output_zip.read(LAYOUT_PATH).decode("utf-16-le"))
        validated_theme = json.loads(output_zip.read(THEME_PATH).decode("utf-8"))
        output_model_hash = hashlib.sha256(output_zip.read("DataModel")).hexdigest()
        if source_model_hash != output_model_hash:
            raise ValueError("The semantic model changed during formatting")
        if [len(page["visualContainers"]) for page in validated_layout["sections"]] != [11, 9, 6]:
            raise ValueError("Unexpected formatted visual counts")
        if validated_theme["name"] != "Coding-Forge Finance Executive":
            raise ValueError("Theme validation failed")
    print(f"Created {OUTPUT.name}; semantic model SHA-256 unchanged: {output_model_hash}")


if __name__ == "__main__":
    build()