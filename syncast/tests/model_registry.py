from django.apps import apps
from django.db import models, connection
from collections import defaultdict

_registered_models = {}
_model_tables_created = set()

# def ensure_model_table(model):
#     if model in _model_tables_created:
#         return
#     with connection.schema_editor() as schema_editor:
#         try:
#             schema_editor.create_model(model)
#             _model_tables_created.add(model)
#         except Exception:
#             pass  # already exists or failed silently



_model_tables_created = set()
_m2m_tables_created = set()
_registered_models = set()

def ensure_model_table(model):
    if model in _model_tables_created:
        return

    with connection.schema_editor() as schema_editor:
        try:
            schema_editor.create_model(model)
            _model_tables_created.add(model)

            # ✅ M2M through tables created once
            for m2m in model._meta.local_many_to_many:
                through = m2m.remote_field.through
                if through._meta.auto_created and through not in _m2m_tables_created:
                    schema_editor.create_model(through)
                    _m2m_tables_created.add(through)

        except Exception as e:
            print(f"❌ Error creating model: {model.__name__} → {e}")



def create_concrete_model(abstract_model, app_label="syncast_test", model_name=None):
    name = model_name or f"Test{abstract_model.__name__.replace('Abstract', '')}"

    model_key = f"{app_label}.{name}"
    if model_key in _registered_models:
        return apps.get_model(app_label, name)

    # ... field and Meta generation ...

    model = type(name, (abstract_model,), {
        "__module__": __name__,
        "Meta": Meta,
        "__test__": False,
        **attrs,  # includes M2M/FK fields if overridden
    })

    # Suppress warning and register only once
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        apps.register_model(app_label, model)

    _registered_models.add(model_key)
    return model


# def create_concrete_model(abstract_model, app_label="syncast_test", model_name=None):
#     name = model_name or f"Test{abstract_model.__name__.replace('Abstract', '')}"
#     model_key = f"{app_label}.{name}"

#     if model_key in _registered_models:
#         return _registered_models[model_key]

#     try:
#         return apps.get_model(app_label, name)
#     except LookupError:
#         pass

#     attrs = {}

#     # Patch FK, O2O, M2M to use concrete targets
#     for field in abstract_model._meta.fields + abstract_model._meta.many_to_many:
#         if isinstance(field, (models.ForeignKey, models.OneToOneField, models.ManyToManyField)):
#             to_model = field.remote_field.model
#             if isinstance(to_model, str):
#                 continue

#             name_, path_, args, kwargs = field.deconstruct()

#             if getattr(to_model._meta, "abstract", False):
#                 concrete_target = create_concrete_model(to_model, app_label)
#                 kwargs["to"] = concrete_target

#             new_field = field.__class__(*args, **kwargs)
#             attrs[field.name] = new_field

#     Meta = type("Meta", (), {
#         "app_label": app_label,
#         "managed": True,
#     })

#     attrs.update({
#         "__module__": __name__,
#         "Meta": Meta,
#         "__test__": False,
#     })

#     model = type(name, (abstract_model,), attrs)

#     try:
#         apps.register_model(app_label, model)
#     except RuntimeError:
#         pass  # Already registered warning is expected in test loop

#     _registered_models[model_key] = model
#     ensure_model_table(model)
#     return model


# def materialize_model(abstract_model, app_label="syncast_test", model_name=None):
#     model = create_concrete_model(abstract_model, app_label, model_name)
#     ensure_model_table(model)
#     return model

def materialize_model(abstract_model, app_label="syncast_test", model_name=None):
    model = create_concrete_model(abstract_model, app_label, model_name)

    # ✅ Create table if missing
    with connection.schema_editor() as schema_editor:
        try:
            schema_editor.create_model(model)
        except Exception:
            pass  # Already created, or not needed

    return model
