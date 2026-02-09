Installation
============

DotZen supports Python 3.8+ and can be installed via pip. Choose the installation method that best suits your needs.

Requirements
------------

**Minimum Requirements:**

* Python 3.8 or higher
* pip (Python package installer)

**Operating Systems:**

* Linux
* macOS
* Windows

Basic Installation
------------------

Install the core DotZen library with zero dependencies:

.. code-block:: bash

   pip install dotzen

This gives you access to:

* Environment variable configuration
* ``.env`` file support
* JSON configuration files
* Docker secrets
* Type casting and validation
* All core design patterns

Verify Installation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import dotzen
   print(dotzen.__version__)

.. code-block:: bash

   # make dotzen is installed
   dotzen --version

Installation with Cloud Providers
----------------------------------

If you need cloud secrets manager support, install the appropriate extras:

AWS Secrets Manager
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install dotzen

**Includes:**

* ``boto3`` - AWS SDK for Python
* ``botocore`` - Low-level AWS client library

Google Cloud Secret Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install dotzen

**Includes:**

* ``google-cloud-secret-manager`` - GCP Secret Manager client

Azure Key Vault
~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install dotzen

**Includes:**

* ``azure-keyvault-secrets`` - Azure Key Vault client
* ``azure-identity`` - Azure authentication

HashiCorp Vault
~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install dotzen

**Includes:**

* ``hvac`` - HashiCorp Vault client

All Cloud Providers
~~~~~~~~~~~~~~~~~~~

Install support for all cloud providers at once:

.. code-block:: bash

   pip install dotzen

Installation with File Format Support
--------------------------------------

Extend DotZen with additional configuration file format support:

YAML Support
~~~~~~~~~~~~

.. code-block:: bash

   pip install dotzen

**Includes:**

* ``PyYAML`` - YAML parser and emitter

TOML Support
~~~~~~~~~~~~

.. code-block:: bash

   pip install dotzen

**Includes:**

* ``tomli`` - TOML parser (Python < 3.11)

JSON5 Support
~~~~~~~~~~~~~

.. code-block:: bash

   pip install dotzen

**Includes:**

* ``json5`` - JSON5 parser

All Formats
~~~~~~~~~~~

Install support for all file formats:

.. code-block:: bash

   pip install dotzen

Complete Installation
---------------------

Install everything (all cloud providers and file formats):

.. code-block:: bash

   pip install dotzen

This is the recommended installation for maximum flexibility.

Development Installation
------------------------

For contributing to DotZen or running tests:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/carrington-dev/dotzen.git
   cd dotzen

   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in editable mode with dev dependencies
   pip install -e ".[dev,test,all]"

   # Install pre-commit hooks
   pre-commit install

Development Extras
~~~~~~~~~~~~~~~~~~

**Available development extras:**

.. code-block:: bash

   pip install dotzen     # Development tools
   pip install dotzen    # Testing tools
   pip install dotzen    # Documentation building

Docker Installation
-------------------

Using DotZen in a Docker container:

.. code-block:: dockerfile

   FROM python:3.12-slim

   # Install DotZen
   RUN pip install dotzen

   # Copy your application
   COPY . /app
   WORKDIR /app

   CMD ["python", "main.py"]

With docker-compose:

.. code-block:: yaml

   version: '3.8'
   services:
     app:
       build: .
       environment:
         - DEBUG=true
         - DATABASE_URL=postgresql://user:pass@db:5432/dbname
       secrets:
         - db_password
         - api_key

   secrets:
     db_password:
       file: ./secrets/db_password.txt
     api_key:
       file: ./secrets/api_key.txt

Virtual Environment Setup
--------------------------

Using venv
~~~~~~~~~~

.. code-block:: bash

   # Create virtual environment
   python -m venv dotzen-env

   # Activate (Linux/macOS)
   source dotzen-env/bin/activate

   # Activate (Windows)
   dotzen-env\Scripts\activate

   # Install DotZen
   pip install dotzen

Using conda
~~~~~~~~~~~

.. code-block:: bash

   # Create conda environment
   conda create -n dotzen python=3.12

   # Activate environment
   conda activate dotzen

   # Install DotZen
   pip install dotzen

Using Poetry
~~~~~~~~~~~~

.. code-block:: bash

   # Initialize project
   poetry init

   # Add DotZen
   poetry add dotzen

   # Add with extras
   poetry add dotzen

   # Install dependencies
   poetry install

Using Pipenv
~~~~~~~~~~~~

.. code-block:: bash

   # Create Pipfile
   pipenv install dotzen

   # Activate virtual environment
   pipenv shell

Requirements File
-----------------

For reproducible installations, create a ``requirements.txt``:

.. code-block:: text

   # requirements.txt
   dotzen==0.1.1
   
   # Or specify exactly what you need
   dotzen==0.1.1
   boto3>=1.26.0          # For AWS
   PyYAML>=6.0            # For YAML files

Install from requirements:

.. code-block:: bash

   pip install -r requirements.txt

Upgrading
---------

Upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade dotzen

   # Or with extras
   pip install --upgrade dotzen

Uninstallation
--------------

Remove DotZen:

.. code-block:: bash

   pip uninstall dotzen

Troubleshooting
---------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue: pip not found**

.. code-block:: bash

   # Install pip
   python -m ensurepip --upgrade

**Issue: Permission denied**

.. code-block:: bash

   # Use --user flag
   pip install --user dotzen

   # Or use virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate
   pip install dotzen

**Issue: SSL Certificate errors**

.. code-block:: bash

   # Upgrade pip
   pip install --upgrade pip

   # Or use trusted host
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org dotzen

**Issue: Dependency conflicts**

.. code-block:: bash

   # Create fresh virtual environment
   python -m venv fresh-env
   source fresh-env/bin/activate
   pip install dotzen

Platform-Specific Notes
-----------------------

Linux
~~~~~

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3-pip python3-venv

   # Fedora/RHEL
   sudo dnf install python3-pip

   # Install DotZen
   pip3 install dotzen

macOS
~~~~~

.. code-block:: bash

   # Using Homebrew
   brew install python3

   # Install DotZen
   pip3 install dotzen

Windows
~~~~~~~

.. code-block:: powershell

   # Download Python from python.org
   # Then in PowerShell or CMD:
   
   python -m pip install --upgrade pip
   pip install dotzen

Verification
------------

Verify your installation:

.. code-block:: python

   import dotzen
   from dotzen import ConfigBuilder, ConfigFactory, config

   # Check version
   print(f"DotZen version: {dotzen.__version__}")

   # Test basic functionality
   import os
   os.environ['TEST_VAR'] = 'Hello, DotZen!'
   
   result = config('TEST_VAR')
   print(f"Config test: {result}")
   
   # Success!
   print("✅ DotZen is installed and working!")

Run the verification script:

.. code-block:: bash

   python -c "import dotzen; print(f'DotZen {dotzen.__version__} installed successfully!')"

Next Steps
----------

Now that DotZen is installed, continue to:

* :doc:`quickstart` - Get started with your first configuration
* :doc:`configuration_sources` - Learn about different config sources
* :doc:`examples` - See real-world usage examples

For more help, see:

* `GitHub Issues <https://github.com/carrington-dev/dotzen/issues>`_
* `Documentation <https://dotzen.readthedocs.io>`_
* `PyPI Page <https://pypi.org/project/dotzen/>`_