.. DotZen documentation master file

DotZen Documentation
====================

**Peaceful, type-safe Python configuration that just works.**

.. image:: https://badge.fury.io/py/dotzen.svg
   :target: https://badge.fury.io/py/dotzen
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/dotzen.svg
   :target: https://pypi.org/project/dotzen/
   :alt: Python Support

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

DotZen brings **zen** to Python configuration management. Load settings from environment variables, 
``.env`` files, JSON, YAML, or cloud secret managers with automatic type casting, validation, and 
a beautiful fluent API.

**No more config chaos. Just pure zen.** 🧘‍♂️✨

.. code-block:: python

   from dotzen import config

   # Simple, elegant, type-safe
   DEBUG = config('DEBUG', cast=bool, default=False)
   PORT = config('PORT', cast=int, default=8000)
   DATABASE_URL = config('DATABASE_URL')
   ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=list)

Quick Links
-----------

* **Getting Started**: :doc:`installation` → :doc:`quickstart`
* **User Guide**: :doc:`user_guide`
* **API Reference**: :doc:`api_reference`
* **Examples**: :doc:`examples`

Key Features
------------

✨ **Unified API** - One interface for all configuration sources

🛡️ **Type Safety** - Automatic casting with validation

🌐 **Multi-Source** - Environment, files, cloud secrets, Docker

✅ **Validation** - Catch errors early, not in production

🏗️ **Design Patterns** - Built on proven architectural patterns

🪶 **Zero Core Dependencies** - Lightweight and fast

🔌 **Extensible** - Easy custom sources and validators

Why DotZen?
-----------

Traditional configuration management is stressful:

* 😫 Scattered config sources (env vars, files, secrets)
* 🔢 Type conversion headaches (strings everywhere!)
* 💥 No validation until runtime failures
* 🔁 Duplicated code across projects
* 🔓 Security risks with hardcoded secrets

DotZen solves these problems with:

* **Chain of Responsibility** - Priority-based value resolution
* **Strategy Pattern** - Pluggable configuration sources
* **Builder Pattern** - Fluent configuration construction
* **Type Safety** - Automatic casting and validation
* **Cloud-Native** - First-class support for AWS, GCP, Azure

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   user_guide

.. toctree::
   :maxdepth: 2
   :caption: Configuration

   configuration_sources
   type_casting
   validation
   cloud_secrets

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   design_patterns
   examples
   api_reference

.. toctree::
   :maxdepth: 1
   :caption: Reference

   contributing
   changelog
   faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
