from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT_ROOT = ROOT / "Completed_Report.Report"
MODEL_ROOT = ROOT / "Completed_Report.SemanticModel"
PAGES_ROOT = REPORT_ROOT / "definition" / "pages"
THEME_PATH = (
    REPORT_ROOT
    / "StaticResources"
    / "SharedResources"
    / "BaseThemes"
    / "Fluent2-CY26SU08.json"
)

PAGE_LAYOUTS = {
    "Financial Health": {
        "a3ee77d504e1ec750277": (64, 112, 420, 132),
        "0e3c5398997758000b7c": (508, 112, 420, 132),
        "a26f7fbc5351c40c162b": (952, 112, 420, 132),
        "0fcce04c43cee40900b9": (1396, 112, 420, 132),
        "da5fa4e95370ec6110db": (1552, 278, 264, 100),
        "7ddecd80a30010d02d61": (1552, 398, 264, 100),
        "7f20d4c300e91c2d3e20": (1552, 518, 264, 100),
        "c6d99db22b474cd647a9": (64, 278, 720, 340),
        "0ed28cab2e665090925a": (808, 278, 720, 340),
        "f21c569293185e9ed359": (64, 650, 1752, 366),
    },
    "Procurement Exposure": {
        "2466d2d4e7269aba9246": (64, 112, 850, 140),
        "c972dc8c41b476628228": (938, 112, 280, 140),
        "b3c2a7ed352632e7362d": (1230, 112, 268, 140),
        "f2452c135013de4d24ee": (1510, 112, 306, 140),
        "4a78137563474092b9a0": (64, 284, 700, 300),
        "266850fb5c758203c620": (788, 284, 600, 300),
        "788dec53b093be321515": (1412, 284, 404, 300),
        "e0fa82009eda690dec68": (64, 616, 1752, 400),
    },
    "Executive Review": {
        "a11f1a1c1a1f1a1c1a1f": (1320, 28, 224, 56),
        "b22e2b2d2b2e2b2d2b2e": (1568, 28, 248, 56),
        "0fc813ea806b09806a19": (64, 112, 1050, 150),
        "33a7a3e128000464a3d0": (1138, 112, 330, 150),
        "9069a3e89985d73e0181": (1492, 112, 324, 150),
        "5061768719e210429be3": (64, 294, 760, 722),
        "4d5fb09c92907e2862d6": (848, 294, 968, 722),
    },
}

VISUAL_TITLES = {
    "c6d99db22b474cd647a9": "Budget vs. Actual by Program",
    "0ed28cab2e665090925a": "Actual Spend Trend by Fiscal Period",
    "f21c569293185e9ed359": "Budget Variance by Program and Fiscal Period",
    "4a78137563474092b9a0": "Outstanding Commitment by Vendor",
    "266850fb5c758203c620": "Purchase Order Value by Program",
    "788dec53b093be321515": "Purchase Orders by Status",
    "e0fa82009eda690dec68": "Purchase Order Detail",
    "5061768719e210429be3": "Budget Variance by Program",
    "4d5fb09c92907e2862d6": "Executive Financial and Procurement Summary",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def literal(value: str) -> dict:
    return {"expr": {"Literal": {"Value": value}}}


def directory_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(file_path.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_path.read_bytes())
    return digest.hexdigest()


def set_position(document: dict, position: tuple[int, int, int, int]) -> None:
    x, y, width, height = position
    document["position"].update(x=x, y=y, width=width, height=height)


def set_title(document: dict, title: str) -> None:
    objects = document["visual"].setdefault("visualContainerObjects", {})
    objects["title"] = [
        {
            "properties": {
                "show": literal("true"),
                "text": literal(f"'{title}'"),
            }
        }
    ]


def format_page(page_path: Path) -> list[dict]:
    page = read_json(page_path)
    page_name = page["displayName"]
    page["height"] = 1080
    page["width"] = 1920
    page["displayOption"] = "FitToPage"
    page["objects"] = {
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
    write_json(page_path, page)

    layouts = PAGE_LAYOUTS[page_name]
    visual_documents = []
    visual_root = page_path.parent / "visuals"
    for visual_path in sorted(visual_root.glob("*/visual.json")):
        document = read_json(visual_path)
        visual_id = document["name"]
        if visual_id not in layouts:
            raise ValueError(f"Unexpected visual {visual_id} on {page_name}")
        set_position(document, layouts[visual_id])
        if visual_id in VISUAL_TITLES:
            set_title(document, VISUAL_TITLES[visual_id])
        write_json(visual_path, document)
        visual_documents.append(document)

    if set(layouts) != {document["name"] for document in visual_documents}:
        raise ValueError(f"Missing visual on {page_name}")
    return visual_documents


def format_theme() -> None:
    theme = read_json(THEME_PATH)
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
        foregroundNeutralSecondary="#5B6573",
        secondaryBackground="#F4F6F8",
        tableAccent="#16324F",
        accent="#2A7F8E",
        shapeStroke="#D8E0E7",
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
        show=True,
        transparency=0,
        color={"solid": {"color": "#FFFFFF"}},
    )
    global_styles["border"][0].update(
        show=True,
        width=1,
        radius=6,
        color={"solid": {"color": "#D8E0E7"}},
    )
    global_styles["dropShadow"][0]["show"] = False
    for axis in ("categoryAxis", "valueAxis"):
        global_styles[axis][0].update(
            gridlineColor={"solid": {"color": "#E7EBEF"}},
            labelColor={"solid": {"color": "#4B5563"}},
        )

    cards = theme["visualStyles"]["cardVisual"]["*"]
    cards["borderCustom"][0].update(
        show=True,
        borderWeight=1,
        borderColor="#D8E0E7",
    )
    cards["shapeCustomRectangle"][0]["rectangleRoundedCurve"] = 6
    cards["label"][0].update(
        fontSize=11,
        fontColor={"solid": {"color": "#5B6573"}},
    )

    for visual_type in ("tableEx", "pivotTable"):
        styles = theme["visualStyles"][visual_type]["None"]
        styles["columnHeaders"][0].update(
            fontColor={"solid": {"color": "#FFFFFF"}},
            backColor={"solid": {"color": "#16324F"}},
        )
        if "rowHeaders" in styles:
            styles["rowHeaders"][0].update(
                fontColor={"solid": {"color": "#17212B"}},
                backColor={"solid": {"color": "#F4F6F8"}},
            )
        styles["values"][0].update(
            backColorPrimary={"solid": {"color": "#FFFFFF"}},
            backColorSecondary={"solid": {"color": "#F7F9FB"}},
        )
    write_json(THEME_PATH, theme)


def validate_geometry(page_name: str, documents: list[dict]) -> None:
    for document in documents:
        position = document["position"]
        if position["x"] < 0 or position["y"] < 0:
            raise ValueError(f"Negative position on {page_name}: {document['name']}")
        if position["x"] + position["width"] > 1920:
            raise ValueError(f"Visual exceeds page width: {document['name']}")
        if position["y"] + position["height"] > 1080:
            raise ValueError(f"Visual exceeds page height: {document['name']}")

    for index, left in enumerate(documents):
        left_position = left["position"]
        for right in documents[index + 1 :]:
            right_position = right["position"]
            overlaps = not (
                left_position["x"] + left_position["width"] <= right_position["x"]
                or right_position["x"] + right_position["width"] <= left_position["x"]
                or left_position["y"] + left_position["height"] <= right_position["y"]
                or right_position["y"] + right_position["height"] <= left_position["y"]
            )
            if overlaps:
                raise ValueError(
                    f"Visual overlap on {page_name}: {left['name']} and {right['name']}"
                )


def build() -> None:
    model_hash = directory_hash(MODEL_ROOT)
    page_documents = {}
    for page_path in sorted(PAGES_ROOT.glob("*/page.json")):
        page_name = read_json(page_path)["displayName"]
        page_documents[page_name] = format_page(page_path)
    format_theme()

    if set(page_documents) != set(PAGE_LAYOUTS):
        raise ValueError("Unexpected report pages")
    for page_name, documents in page_documents.items():
        validate_geometry(page_name, documents)
        for document in documents:
            visual_id = document["name"]
            if visual_id in VISUAL_TITLES:
                title = document["visual"]["visualContainerObjects"]["title"][0]
                expected = f"'{VISUAL_TITLES[visual_id]}'"
                if title["properties"]["text"]["expr"]["Literal"]["Value"] != expected:
                    raise ValueError(f"Title validation failed: {visual_id}")

    for json_path in REPORT_ROOT.rglob("*.json"):
        read_json(json_path)
    if directory_hash(MODEL_ROOT) != model_hash:
        raise ValueError("The semantic model changed during report formatting")
    print(
        "Formatted PBIP report: "
        f"{sum(len(items) for items in page_documents.values())} visuals, "
        f"{len(VISUAL_TITLES)} explicit titles, semantic model unchanged ({model_hash})."
    )


if __name__ == "__main__":
    build()