class EnforcedFKTargetsMixin:
    """
    Mixin to enforce that concrete subclasses define ForeignKeys 
    to specific base models.

    This ensures coupling and schema design rules across projects 
    using abstract base classes.
    """

    # List of required FK targets to be enforced.
    # Each item is a dotted path to an abstract model (e.g. 'syncast.models.scope.AbstractSyncCastScope')
    REQUIRED_FK_TARGETS = []

    @classmethod
    def check(cls, **kwargs):
        from django.core.checks import Error
        from django.utils.module_loading import import_string
        from django.db import models

        errors = super().check(**kwargs)

        if cls._meta.abstract:
            return errors

        # Get all ForeignKey fields on this model
        fks = [f for f in cls._meta.fields if isinstance(f, models.ForeignKey)]

        # Loop through each required base path and enforce presence of a matching FK
        for path in getattr(cls, "REQUIRED_FK_TARGETS", []):
            try:
                expected_base = import_string(path)
            except ImportError:
                # Could not import the required model — raise check error
                errors.append(
                    Error(f"Could not import base class {path}", id="syncast.E004")
                )
                continue

            if not any(issubclass(f.remote_field.model, expected_base) for f in fks):
                errors.append(
                    Error(
                        f"{cls.__name__} must define a ForeignKey to a subclass of {path}.",
                        id=f"syncast.E003.{expected_base.__name__}",
                    )
                )

        return errors
