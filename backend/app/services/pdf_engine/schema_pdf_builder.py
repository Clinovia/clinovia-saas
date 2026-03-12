from typing import Type
import json
from pydantic import BaseModel


def schema_to_table(schema: Type[BaseModel], values: dict):
    """
    Converts a Pydantic schema + values into a PDF table.
    """

    rows = [["Field", "Value"]]

    for field_name, field in schema.model_fields.items():

        label = field.title or field_name.replace("_", " ").title()

        value = values.get(field_name)

        if value is None:
            value = "—"

        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=2)

        rows.append([label, str(value)])

    return rows