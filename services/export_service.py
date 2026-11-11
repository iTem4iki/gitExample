import csv
import json
import os
import xml.etree.ElementTree as ET

import yaml

from repositories import export_repository


def _flatten(item: dict, prefix: str = "") -> dict:
    # для CSV: вложенные поля объединяем в одну строку (client_login и т.д.)
    flat = {}
    for key, value in item.items():
        name = prefix + key
        if isinstance(value, dict):
            flat.update(_flatten(value, name + "_"))
        elif isinstance(value, list):
            flat[name] = ";".join(str(v) for v in value)
        else:
            flat[name] = value
    return flat


def _fill_xml(parent: ET.Element, key: str, value):
    # рекурсивно превращаем словарь / список / значение в XML-элементы
    element = ET.SubElement(parent, key)
    if isinstance(value, dict):
        for k, v in value.items():
            _fill_xml(element, k, v)
    elif isinstance(value, list):
        for v in value:
            _fill_xml(element, "item", v)
    elif value is not None:
        element.text = str(value)


def save_json(rows: list, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def save_csv(rows: list, path: str):
    flat_rows = [_flatten(r) for r in rows]
    # заголовок собираем по всем строкам: у части заявок может не быть оператора
    fields = []
    for row in flat_rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    # убираем пустышку operator (когда оператора нет), если есть operator_id и т.п.
    fields = [f for f in fields
              if not (all(row.get(f) is None for row in flat_rows)
                      and any(o.startswith(f + "_") for o in fields))]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(flat_rows)


def save_xml(rows: list, path: str, root_name: str, item_name: str):
    root = ET.Element(root_name)
    for row in rows:
        _fill_xml(root, item_name, row)
    ET.indent(root)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def save_yaml(rows: list, path: str):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(rows, f, allow_unicode=True, sort_keys=False)


def export_all(folder: str = "out", root_name: str = "requests",
               item_name: str = "request") -> list[str]:
    rows = export_repository.get_export_rows()
    os.makedirs(folder, exist_ok=True)

    files = {
        "data.json": lambda p: save_json(rows, p),
        "data.csv": lambda p: save_csv(rows, p),
        "data.xml": lambda p: save_xml(rows, p, root_name, item_name),
        "data.yaml": lambda p: save_yaml(rows, p),
    }
    created = []
    for name, save in files.items():
        path = os.path.join(folder, name)
        save(path)
        created.append(path)
    return created
