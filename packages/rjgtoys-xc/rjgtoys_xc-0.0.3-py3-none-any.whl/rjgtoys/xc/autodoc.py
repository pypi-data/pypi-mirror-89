from typing import Any, get_type_hints


import json


from sphinx.ext.autodoc import ExceptionDocumenter
from sphinx.util import logging
from sphinx.locale import _, __

from sphinx_autodoc_typehints import format_annotation

from rjgtoys.xc import XC
from rjgtoys.xc._xc import _XCType, ImpliedFieldInfo


logger = logging.getLogger(__name__)


class XCDocumenter(ExceptionDocumenter):
    """
    Specialized ExceptionDocumenter subclass for XC exceptions.
    """

    objtype = 'exception'
    directivetype = 'exception'
    member_order = 10

    # needs a higher priority than ClassDocumenter and ExceptionDocumenter
    priority = 15

    @classmethod
    def can_document_member(
        cls, member: Any, membername: str, isattr: bool, parent: Any
    ) -> bool:
        return isinstance(member, type) and issubclass(member, XC)

    def get_base_description(self):

        if not hasattr(self.object, '__bases__') or not len(self.object.__bases__):
            print(
                "Could not identify bases for %s.%s"
                % (self.object.__module__, self.object.__name__)
            )
            return ""

        bases = [
            ':class:`%s.%s`' % (b.__module__, b.__name__) for b in self.object.__bases__
        ]
        return ', '.join(bases)

    def generate(
        self,
        more_content: Any = None,
        real_modname: str = None,
        check_module: bool = False,
        all_members: bool = False,
    ) -> None:
        """Generate reST for the object given by *self.name*, and possibly for
        its members.

        If *more_content* is given, include that content. If *real_modname* is
        given, use that module name to find attribute docs. If *check_module* is
        True, only generate if the object is defined in the module name it is
        imported from. If *all_members* is True, document all members.
        """
        if not self.parse_name():
            # need a module to import
            logger.warning(
                __(
                    'don\'t know which module to import for autodocumenting '
                    '%r (try placing a "module" or "currentmodule" directive '
                    'in the document, or giving an explicit module name)'
                )
                % self.name,
                type='autodoc',
            )
            return

        # now, import the module and get object to document
        if not self.import_object():
            return

        # Is this the right kind?  If not, delegate to the superclass.

        if not isinstance(self.object, _XCType):
            super().generate(
                more_content=more_content,
                real_modname=real_modname,
                check_module=check_module,
                all_members=all_members,
            )
            return

        # hackery to get at the kind of field each is,
        # in particular, to identify 'implied' fields.
        #

        implied_fields = set()
        for (name, mf) in self.object._model.__fields__.items():
            print(name)
            #print(f"  {mf.field_info.__class__.__name__} {mf.field_info}")
            if isinstance(mf.field_info, ImpliedFieldInfo):
                implied_fields.add(name)

        schema = self.object._model.schema()

        try:
            hints = get_type_hints(self.object._model)
        except Exception as e:
            print("Get type hints for %s: %s" % (self.fullname, e))
            hints = {}

        source = "description of %s" % (self.object_name)

        sig = "(%s)" % (", ".join(p for p in schema['properties'] if p not in implied_fields))

        self.add_directive_header(sig)

        self.add_line('', source)

        indent = self.indent
        try:
            self.indent += '   '

            try:
                descr = schema['description']
            except KeyError:
                descr = f'Object {self.object_name} has neither description nor title'

            for (i, line) in enumerate(descr.splitlines()):
                self.add_line(line.strip(), source, i)

            # Always do 'show-inheritance'

            bases = self.get_base_description()

            if bases:
                self.add_line('', source)
                self.add_line("A subclass of %s" % (bases), source)

            self.add_line('', source)

            source = self.get_sourcename()

            has_params = False
            for (pname, ptype) in schema['properties'].items():

                if pname in implied_fields: # we'll do implied fields in the next pass
                    continue

                if not has_params:
                    self.add_line('Attributes (passed as parameters):', source)

                has_params = True

                hint = hints.get(pname, '')
                if hint:
                    hint = format_annotation(hint)
                else:
                    hint = '(unspecified)'

                self.add_line('  :py:attr:`%s` (%s) - %s' % (pname, hint, ptype['title']), source)

                self.add_line('', source)

            # Second pass, describe implied parameters/properties

            if implied_fields:
                if has_params:
                    self.add_line('Additional attributes:', source)
                else:
                    self.add_line('Attributes:', source)

                for pname in implied_fields:
                    ptype = schema['properties'][pname]

                    hint = hints.get(pname, '')
                    if hint:
                        hint = format_annotation(hint)
                    else:
                        hint = '(unspecified)'

                    print(hint)
                    self.add_line('  :py:attr:`%s` (%s) - %s' % (pname, hint, ptype['title']), source)

                    self.add_line('', source)

            subclasses = self.object.__subclasses__()

            # Add the attributes

            # For a base class, the only inherited property that's of interest
            # is the status

            if subclasses:
                show_props = (
                    ('status','int'),
                )
            else:
                show_props = (
                    ('typename', 'str'),
                    ('title', 'str'),
                    ('detail', 'str'),
                    ('status', 'int')
                )

            self.add_line('Class attributes (read-only):', source)

            for (name, hint) in show_props:
                self.add_line(
                    '  :py:attr:`%s` (:py:class:`%s`) = %s'
                    % (name, hint, repr(getattr(self.object, name, '(not set)'))),
                    source,
                )
                self.add_line('', source)

            if subclasses:
                self.add_line('', source)
                self.add_line('Subclasses:', source)
                self.add_line('', source)

                for sub in subclasses:
                    self.add_line(' - :exc:`%s`' % (sub.__name__), source)
                    self.add_line('', source)

        finally:
            self.indent = indent

        return

        # DEBUG: dump our output

        for line in self.directive.result:
            print("RESULT: %s" % (line))


class StdExceptionDocumenter(ExceptionDocumenter):
    """A replacement for the standard ExceptionDocumenter
    that exists just to create a new directive that
    can be used in the XC docs themselves.

    It creates an 'autoxc_as_exception::' directive
    that does what the standard `autoexception::` does.

    """

    objtype = "xc_as_exception"
    directivetype = "exception"


def setup(app):
    # Ensure prerequisites are loaded first
    app.setup_extension('sphinx.ext.autodoc')
    app.setup_extension('sphinx_autodoc_typehints')

    app.add_autodocumenter(XCDocumenter, override=True)
    app.add_autodocumenter(StdExceptionDocumenter)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
