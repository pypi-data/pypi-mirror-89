"""
Control imports for XC
"""

import urllib

from ._xc import _XCBase, _XCType, _XCFormatter, Title, Implied

from ._raises import raises, may_raise, raises_exception

from ._json import json_loads, json_dumps

__all__ = (
    'XC',
    'Error',
    'Title',
    'Implied',
    'raises',
    'may_raise',
    'raises_exception',
    'BadExceptionBug',
    'BadExceptionsInTestBug'
)

# The following are put here simply so that their fully qualified
# names do not include _xc


class XC(_XCBase, metaclass=_XCType):
    """The base class for 'structured' exceptions.

    Provides a bit of structure on top of the language-provided
    :class:`Exception`.

    Each (sub-)class defines a set of parameters that are become
    attributes of the exception, available to handlers.

    Those parameters are type-checked and may have associated
    defaults and descriptions that are available to generate
    documentation and other forms of help.

    In particular, :class:`XC` subclasses can be serialised
    and deserialised as described in RFC7807, which makes
    them easy to use for building REST APIs.

    Each subclass should define the following attributes:

    typename
      The 'problem identifier' - defaults to the name of the class.

      This is used to generate the RFC7807 `type` attribute.

      If no value is set explicitly, the fully qualified name of the class is used.
    title
      A short human-readable description of the problem type.

      This is used as the RFC7807 `title` attribute.
    detail
      A format template that can produce a human-readable explanation
      specific to a particular instance of this exception.

      This is used to define the string representation of the exception (the `__str__` method)
      and also (via :func:`str`) to generate the RFC7807 `detail` attribute.
    status
      An HTTP status code associated with this exception.  Defaults to 400.

      This is used when the exception is transported over HTTP.

    The above attributes are defined in RFC 7807.

    """

    # The following are magically kept in the exception class, not the content

    typename: str
    title: str

    detail: str

    status: int = 400

    def __str__(self):
        try:
            fmt = _XCFormatter(self)
            return fmt.format(self.detail)
            return self.detail.format(**self._content.dict())
        except Exception as e:
            return "%s.__str__() -> %s" % (self.__class__.__name__, e)

    def to_dict(self):
        """Produce a JSON-encodable dict representing this exception.

        Returns an RFC7807-compliant JSON object.
        """

        content = self._content.dict()
        data = dict(
            type=self.typename,
            title=self.title,
            status=self.status,
            detail=str(self),
            instance="%s?%s" % (self.typename, urllib.parse.urlencode(content)),
            content=content,
        )
        return data

    @classmethod
    def from_obj(cls, data):
        """Reconstruct an exception from some data.

        Expects an object such as might be produced by
        parsing the result of calling :meth:`to_json()` on
        an instance of this class or a subclass of it.

        Returns an instance of the appropriate class, or
        raises :exc:`TypeError` if no class can be identified.
        """

        typename = data['type']

        for kls in all_subclasses(cls):
            if kls.typename == typename:
                return kls(**data['content'])

        raise TypeError("No %s type %s" % (cls.__name__, typename))

    @classmethod
    def from_json(cls, data):
        return cls.from_obj(json_loads(data))


def all_subclasses(cls):
    # pylint: disable=line-too-long
    # the following comment is simply too wide
    """Generate all subclasses of class `cls`.

    See: https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name
    """

    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )


class Bug(XC):
    """
    This is the base class for exceptions that should never occur at runtime.

    They indicate a programming error that is not recoverable.
    """

    pass


class Error(XC):
    """
    This is the base class for exceptions that may be recoverable.

    Packages should create subclasses of this.
    """

    pass


class _ExceptionField:
    """Allows a Pydantic model to have fields that hold an exception value."""

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, v):
        assert isinstance(v, Exception)
        return v


class BadExceptionBug(Bug):
    """Raised when some function or method raises an exception
    that it has not declared itself capable of raising.

    :param raised: The exception that was raised (and which is
            not in the allowed set)
    """

    raised: _ExceptionField = Title("The disallowed exception")

    detail = "Disallowed exception raised: {raised}"


class BadExceptionsInTestBug(Bug):

    """Raised on an attempt to patch something to
        raise an exception that it is not allowed to raise

    Args:
        name: Name of the object being tested
        exceptions: The exceptions that may not be raised
            by this object
    """

    oneline = "Test case for {name} raises bad exception(s): {exclist}"

    def unpack(self):
        self.exclist = ", ".join(map(repr, self.exceptions))
