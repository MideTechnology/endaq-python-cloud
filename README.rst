*****
endaq-cloud
*****

The `cloud` subpackage for `endaq-python`

TODO: This.

Tools:
=====

API Wrapper:
....
The API Wrapper provides a simple command-line interface for accessing basic file and device information from the enDAQ Cloud API. Output of all commands except ``account`` and `attributes` are in ``csv`` files in the ``output`` folder.

To access the cloud, this tool requires an API key associated with a user's enDAQ Cloud account, which can be provided in two ways:

* (recommended) add to the ``endaq.cloud`` project directory a ``.env`` file, formatted like so::

	API_KEY=<Your Key>

* pass in an API key through the command line using the ``--key`` option

.. warning::
	For security reasons, it is generally discouraged to make an authentication key visible on-screen or accessible through the clipboard, such as when using the ``--key`` option; we provide the ``key`` option solely as a convenience.

Runs on Python 3.6 and higher

Usages:
++++++
-h                  Command Line Help
--id, -i            File or Device ID
--limit, -l         File or Device output limit; Max 100 default 50
--key, -k           API Key
--attributes, -a    Attributes to be outputted; options = all or att1,att2...; default is none
--name, -n          Attribute Name
--type, -t          Attribute Type; options = int, float, string, boolean
--value, -v         Attribute Value

- python API_wrapper.py files -a <ATTRIBUTES_TO_GET> -l <FILE_OR_DEVICE_OUTPUT_LIMIT>
- python API_wrapper.py file-id -i **# additional argument needed**
- python API_wrapper.py devices -l <FILE_OR_DEVICE_OUTPUT_LIMIT>
- python API_wrapper.py device-id -i **# additional argument needed**
- python API_wrapper.py account
- python API_wrapper.py attribute -n <ATTRIBUTE_NAME> -t <ATTRIBUTE_TYPE> -v <ATTRIBUTE_VALUE> -i **# additional arguments needed**
