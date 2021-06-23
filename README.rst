*****
endaq-cloud
*****

The `cloud` subpackage for `endaq-python`

TODO: This.

Tools:
=====

API Wrapper:
....
The API Wrapper is a way to access the enDAQ Cloud API through a command line tool. To use
this tool you need to put your ``API Key`` in a ``.env``: ``API_KEY=<Your Key>``. Or if you would
like you can pass in your API Key through the command line using ``-k`` but that is less
secure than using a ``.env``. Output of all commands except ``account`` and `attributes` are
in ``csv`` files in the ``output`` folder

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

``
- python API_wrapper.py files -a -l
- python API_wrapper.py file-id -i **# additional argument needed**
- python API_wrapper.py devices -l
- python API_wrapper.py device-id -i **# additional argument needed**
- python API_wrapper.py account
- python API_wrapper.py attribute -n -t -v -i **# additional arguments needed**
``