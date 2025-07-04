from django.apps import apps
from django.db import models, connection
 


def create_table_if_not_exists(model):
    table_name = model._meta.db_table

    with connection.cursor() as cursor:
        tables = connection.introspection.table_names()
        if table_name in tables:
            return

    if connection.vendor == "sqlite":
        # Disable FK constraints (required for schema editing with FKs in SQLite)
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = OFF;")

        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(model)
        finally:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_keys = ON;")
    else:
        # Non-SQLite: create as usual
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)


def create_test_model(name, base, fields=None, app_label="testapp"):
    fields = fields or {}

    Meta = type("Meta", (), {"app_label": app_label, "managed": True})
    attrs = {"__module__": f"{app_label}.models", "Meta": Meta, **fields}
    model = type(name, (base,), attrs)

    try:
        apps.get_model(app_label, name)
    except LookupError:
        apps.register_model(app_label, model)

    create_table_if_not_exists(model)
    return model
