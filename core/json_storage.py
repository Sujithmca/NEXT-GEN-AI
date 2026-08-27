import json
import os

from django.conf import settings


DATA_DIR = os.path.join(
    settings.BASE_DIR,
    "data"
)


def get_file_path(filename):

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    return os.path.join(
        DATA_DIR,
        filename
    )


def load_json(filename):

    file_path = get_file_path(filename)

    if not os.path.exists(file_path):

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )

        return []


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_json(filename, data):

    file_path = get_file_path(filename)

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    temp_path = file_path + ".tmp"

    with open(
        temp_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    os.replace(
        temp_path,
        file_path
    )


def get_item(filename, item_id):

    items = load_json(filename)

    return next(
        (
            item for item in items
            if item.get("id") == item_id
        ),
        None
    )


def create_item(filename, item):

    items = load_json(filename)

    existing_ids = [
        item.get("id", 0)
        for item in items
        if isinstance(item.get("id"), int)
    ]

    new_id = (
        max(existing_ids, default=0) + 1
    )

    item["id"] = new_id

    items.append(item)

    save_json(
        filename,
        items
    )

    return item


def update_item(filename, item_id, updated_data):

    items = load_json(filename)

    for index, item in enumerate(items):

        if item.get("id") == item_id:

            updated_data["id"] = item_id

            items[index] = updated_data

            save_json(
                filename,
                items
            )

            return updated_data

    return None


def delete_item(filename, item_id):

    items = load_json(filename)

    new_items = [
        item for item in items
        if item.get("id") != item_id
    ]

    if len(new_items) == len(items):
        return False

    save_json(
        filename,
        new_items
    )

    return True