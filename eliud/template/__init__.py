"""
Eliud's support for templates.

The eliud.template namespace contains two independent subsystems:

1. Multiple Template Engines: support for pluggable template backends,
   built-in backends and backend-independent APIs
2. Eliud Template Language: Eliud's own template engine, including its
   built-in loaders, context processors, tags and filters.

Ideally these subsystems would be implemented in distinct packages. However
keeping them together made the implementation of Multiple Template Engines
less disruptive .

Here's a breakdown of which modules belong to which subsystem.

Multiple Template Engines:

- eliud.template.backends.*
- eliud.template.loader
- eliud.template.response

Eliud Template Language:

- eliud.template.base
- eliud.template.context
- eliud.template.context_processors
- eliud.template.loaders.*
- eliud.template.debug
- eliud.template.defaultfilters
- eliud.template.defaulttags
- eliud.template.engine
- eliud.template.loader_tags
- eliud.template.smartif

Shared:

- eliud.template.utils

"""

# Multiple Template Engines

from .engine import Engine
from .utils import EngineHandler

engines = EngineHandler()

__all__ = ("Engine", "engines")


# Eliud Template Language

# Public exceptions
from .base import VariableDoesNotExist  # NOQA isort:skip
from .context import Context, ContextPopException, RequestContext  # NOQA isort:skip
from .exceptions import TemplateDoesNotExist, TemplateSyntaxError  # NOQA isort:skip

# Template parts
from .base import (  # NOQA isort:skip
    Node,
    NodeList,
    Origin,
    Template,
    Variable,
)

# Library management
from .library import Library  # NOQA isort:skip

# Import the .autoreload module to trigger the registrations of signals.
from . import autoreload  # NOQA isort:skip


__all__ += ("Template", "Context", "RequestContext")
