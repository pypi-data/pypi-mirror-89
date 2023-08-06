"""
Exceptions, particularly those that can be transported
over an HTTP REST API.

.. autoclass:: _XCContentModel
   :members:

.. autoexception:: XC
   :members: to_json, from_json

.. autoclass:: _XCContentModel

.. autoexception:: _XCBase

.. autoclass:: _XCType


"""

import urllib
import json
import string

from typing import Any

from pydantic import BaseModel, Field

from pydantic.fields import FieldInfo

from rjgtoys.xc._json import json_loads, json_dumps


def Title(t):
    """Simplifies model declarations a little."""

    return Field(..., title=t)


class ImpliedFieldInfo(FieldInfo):
    """Subclass to help identify implied fields."""


def Implied(
    alias: str = None,
    title: str = None,
    description: str = None,
    const: bool = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    multiple_of: float = None,
    min_items: int = None,
    max_items: int = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    **extra: Any
    ):
    """Declare a field to be 'implied' - i.e. optional because the
    class will compute a value for itself, if no value is provided.
    """

    return ImpliedFieldInfo(
        None,
        alias=alias,
        title=title,
        description=description,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        min_items=min_items,
        max_items=max_items,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        **extra,
    )

class _XCContentModel(BaseModel):
    """
    This is the base class for exception content - the values
    of parameters passed to their constructors.

    It's essentially :class:`pydantic.BaseModel`.
    """

    class Config:
        arbitrary_types_allowed = True

    pass


"""
The Exception base class and the BaseModel don't
play nicely together; make Exceptions that carry
a BaseModel instance around, so that the two interfaces
can be kept separate.

"""


class _XCBase(Exception):
    """A hidden base class for exceptions."""

    _model = _XCContentModel

    def __init__(self, **kwargs):
        super(_XCBase, self).__init__()

        # Careful with this one because __setattr__ is overridden
        super().__setattr__('_content', self._model.parse_obj(kwargs))

        self._infer()

    def __getattr__(self, name):
        return getattr(self._content, name)

    def __setattr__(self, name, value):
        return setattr(self._content, name, value)

    def _infer(self):
        """An optional method that is intended to add computed attributes to an exception.

        This method is called during construction of the exception, and before
        any of the kwargs have been validated, so there is scope for surprise
        type checking errors.

        When an exception is serialised, all its fields are encoded, including
        the ones that are provided by this method.   So when an exception
        is de-serialised, there is nothing for this method to do; it should
        provide values for any parameters (kwargs) that are missing, but should
        probably not override any that are present.

        For example, if the exception takes a 'hostname' parameter and this
        method is capable of adding an 'ipaddress' field, that should only take
        place if the 'ipaddress' parameter is not passed in.   As a result,
        if an exception is serialised on one host, sent to another, and deserialised
        there, the 'ipaddress' value seen in the destination host will be the value
        that was computed at the sender, not at the recipient.

        """

        pass

    @classmethod
    def parse_json(cls, data):
        return cls(**json_loads(data))

    def __eq__(self, other):
        """Two exceptions are identical if they are the same class and have the same content."""

        return (self.__class__ is other.__class__) and (self._content == other._content)


class _XCType(type):
    """Metaclass for exceptions."""

    def __new__(cls, name, bases, attrs):
        """Generate a new BaseException subclass.

        The attrs passed in are reorganised so that
        most are moved to an internal '_model' class
        that is derived from BaseModel (from the
        _model classes of the bases, in fact).
        """

        # Should this 'fully qualify'?

        qualname = '.'.join((attrs['__module__'], name))
        attrs.setdefault('typename', qualname)
        # Does this 'inherit' correctly?
        if 'title' not in attrs:
            title = attrs.get('__doc__', '\n').splitlines()[0]
            attrs['title'] = title

        exc_attrs = {}
        model_attrs = {}

        exc_attr_forced = ('typename', 'title', 'detail', 'status')

        for (n, v) in attrs.items():

            # Some go only to the exception class

            if n in exc_attr_forced:
                exc_attrs[n] = v
                continue

            if n.startswith('_'):
                exc_attrs[n] = v
                continue

            # Content items can't be callable

            if callable(v) or isinstance(v, (classmethod, staticmethod)):
                exc_attrs[n] = v
                continue

            # Otherwise, move it to model

            model_attrs[n] = v

        # UGLY: fix up the annotations of the model and the exception

        anns = attrs.get('__annotations__', {})

        # Capture annotations of any attributes that were put into the exception
        exc_ann = {k: anns[k] for k in exc_attrs if k in anns}
        # and anyway copy those for the forced attributes
        exc_ann.update({k: anns[k] for k in exc_attr_forced if k in anns})

        exc_attrs['__annotations__'] = exc_ann

        # Move all the rest to the model

        model_ann = {k: v for (k, v) in anns.items() if k not in exc_ann}

        model_attrs['__annotations__'] = model_ann

        #        print("Build %s exception %s from %s" % (cls.__name__, name, attrs))
        #        print("  Exception attrs %s" % (exc_attrs,))
        #        print("  Model attrs %s" % (model_attrs,))

        exc_doc = exc_attrs.get('__doc__', exc_attrs['title'])

        model_attrs['__doc__'] = exc_doc

        # Build the content model class

        model = type('_model', tuple(s._model for s in bases), model_attrs)

        exc_attrs['_model'] = model

        return type.__new__(cls, name, bases, exc_attrs)


class MissingAttributeBug(Exception):
    """Raised when formatting the detail of an exception fails."""

    # It can't be a Bug or Error because those are not available yet.

    def __init__(self, cls, name):
        self.cls = cls
        self.name = name

    def __str__(self):
        return f"'{self.cls.__name__}' exception has no attribute '{self.name}'"


class _XCFormatter(string.Formatter):
    """A special string formatter than can retrieve attributes
    from an exception.   The attributes of an exception are not
    all stored directly on the exception itself, and this hides
    that from the authors of format strings.
    """

    def __init__(self, exc):
        self._exc = exc

    def get_value(self, name, *args, **kwargs):

        try:
            return getattr(self._exc, name)
        except AttributeError:
            raise MissingAttributeBug(cls=self._exc.__class__, name=name)

