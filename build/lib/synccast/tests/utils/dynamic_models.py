# Django imports
from django.apps import apps
from django.db import models, connection
 
def create_table_if_not_exists(model):
    """
    Ensures the database table for the given model exists.
    If it doesn't, it creates the table using Django's schema editor.
    Handles SQLite-specific requirements like disabling foreign key checks.
    """

    # Get the database table name from the model's metadata
    table_name = model._meta.db_table

    # Check if the table already exists in the database
    with connection.cursor() as cursor:
        tables = connection.introspection.table_names()
        if table_name in tables:
            return
        
    # Handle SQLite database quirks
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
    """
    Dynamically creates and registers a new Django model class at runtime.
    
    Args:
        name (str): Name of the new model class.
        base (models.Model): Base class (usually `models.Model` or a subclass).
        fields (dict): Optional dict of field definitions (e.g., {"field1": models.CharField(...)}).
        app_label (str): The label of the app where the model should be registered.

    Returns:
        model: The dynamically created and registered model class.
    """
    fields = fields or {} # Default to empty dict if fields are not provided

    # Define a minimal inner Meta class to specify the app label and management
    Meta = type("Meta", (), {"app_label": app_label, "managed": True})

    # Assemble attributes of the new model class, including Meta
    attrs = {"__module__": f"{app_label}.models", "Meta": Meta, **fields}

    # Dynamically create the model class
    model = type(name, (base,), attrs)

    try:
        apps.get_model(app_label, name)
    except LookupError:
        apps.register_model(app_label, model)

    create_table_if_not_exists(model)
    return model
