import re
import sys
from collections import OrderedDict
from typing import Dict, Optional

import graphene
from django.core.exceptions import ImproperlyConfigured
from graphene.types.mutation import MutationOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.rest_framework.mutation import fields_for_serializer
from graphql import ResolveInfo

from jnt_django_graphene_toolbox.errors import (
    BaseGraphQLError,
    GraphQLInputError,
)


class SerializerMutationOptions(MutationOptions):
    """Serializer mutation options."""

    serializer_class = None


class SerializerMutation(graphene.Mutation):
    """Serializer mutation."""

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(  # noqa: WPS211
        cls,
        serializer_class=None,
        _meta=None,
        only_fields=(),
        exclude_fields=(),
        **options,
    ):
        """Inits subclass with meta."""
        if not serializer_class:
            raise ImproperlyConfigured(
                "serializer_class is required for the SerializerMutation",
            )

        serializer = serializer_class()

        input_fields = fields_for_serializer(
            serializer, only_fields, exclude_fields, is_input=True,
        )

        input_fields = yank_fields_from_attrs(input_fields)

        base_name = re.sub("Payload$", "", cls.__name__)

        if not input_fields:
            input_fields = {}

        cls.Arguments = type(
            "{0}Arguments".format(base_name),
            (object,),
            OrderedDict(input_fields),
        )

        if not _meta:
            _meta = SerializerMutationOptions(cls)  # noqa: WPS122

        _meta.serializer_class = serializer_class

        super().__init_subclass_with_meta__(
            output=None,
            name="{0}Payload".format(base_name),
            _meta=_meta,
            **options,
        )

    @classmethod
    def mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **input,  # noqa: WPS125
    ) -> "SerializerMutation":
        """Mutate handler."""
        try:
            return cls._mutate(root, info, **input)
        except BaseGraphQLError as err:
            err.stack = sys.exc_info()[2]
            return err

    @classmethod
    def mutate_and_get_payload(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110, WPS125
        **input,  # noqa: WPS125
    ) -> "SerializerMutation":
        """Mutate and get payload."""
        kwargs = cls.get_serializer_kwargs(root, info, **input)
        serializer = cls._meta.serializer_class(**kwargs)

        if serializer.is_valid():
            return cls.perform_mutate(root, info, serializer.validated_data)

        raise GraphQLInputError(serializer.errors)

    @classmethod
    def get_serializer_kwargs(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **input,  # noqa: WPS125
    ) -> Dict[str, object]:
        """Get serializer options."""
        return {
            "data": input,
            "context": {"request": info.context},
        }

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data,
    ) -> "SerializerMutation":
        """Overrideable mutation operation."""
        raise NotImplementedError

    @classmethod
    def internal_mutate(
        cls, root, info, **kwargs,  # noqa: WPS110
    ) -> "SerializerMutation":
        """Private mutate handler."""
        return cls.mutate_and_get_payload(root, info, **kwargs)
