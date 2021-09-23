"""
Core enDAQ Cloud communication API

TODO: Rewrite docstrings (pref. before implementing methods)
"""
from typing import Optional, Union

from idelib.dataset import Dataset
from pandas import DataFrame

# ==============================================================================
#
# ==============================================================================

ENV_PRODUCTION = "https://qvthkmtukh.execute-api.us-west-2.amazonaws.com/master"
ENV_STAGING = "https://p377cock71.execute-api.us-west-2.amazonaws.com/staging"

# ==============================================================================
#
# ==============================================================================


class EndaqCloud:
    """
    A representation of a connection to an enDAQ Cloud account, providing a
    high-level interface for accessing its contents.
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 env: Optional[str] = None,
                 test: bool = True):
        """
        Constructor for an `EndaqCloud` object, which provides access to an
        enDAQ Cloud account.

        :param api_key:
        :param env:
        :param test: If `True` (default), the connection to enDAQ Cloud will
            be tested before being returned. A failed test will generate a
            meaningful error message describing the problem.
        """


    def get_file(self,
                 file_id: Union[int, str],
                 local_name: Optional[str] = None) -> Dataset:
        """
        Download the specified file to local_name if provided, use the file
        name from the cloud if no local name is provided.
        TODO: This should be made to match `endaq.ide.get_doc()`

        :param file_id: The file's cloud ID.
        :param local_name:
        :return: The imported file
        """


    def get_file_table(self,
                       attributes: Union[list, str] = "all",
                       limit: int = 100) -> DataFrame:
        """
        Get a table of the data that would be similar to that you'd get doing
        the CSV export on the my recordings page, up to the first `limit`
        files with attributes matching `attributes`.

        :param limit: The maximum number of files to return.
        :param attributes: A list of attribute strings (or a single
            comma-delimited string of attributes) to match.
        :return: A `DataFrame` of file IDs and relevant information.
        """
        # IDEAS:
        #   * Accept regex objects as `attributes` (in addition to strings)
        #   * Accept glob-like patterns (e.g. "GPS Speed:*") using `fnmatch`


    def get_devices(self) -> DataFrame:
        """
        Get dataframe of devices and associated attributes (part_number,
        description, etc.) attached to the account.

        :return: A `DataFrame` of recorder information.
        """


    def set_attributes(self,
                       file_id: Union[int, str],
                       attributes: dict) -> dict:
        """
        Set the 'attributes' (name/value metadata) of a file.

        :param file_id: The file's cloud ID.
        :param attributes:
        :return: The file's new attributes.
        """
        # NOTE: This was called `post_attributes()` in the Confluence docs.
        #  'post' referred to the fact it is a POST request, which is
        #  really an internal detail; 'set' is more appropriate for an API.

        # IDEAS:
        #   * Use `**kwargs` instead of an `attributes` dict?
        #   * Automatically assume type, unless value is a tuple containing (value, type)


# ==============================================================================
#
# ==============================================================================


def count_tags(df: DataFrame) -> DataFrame:
    """
    Given the dataframe returned by `EndaqCloud.get_file_table()`, provide
    some info on the tags of the files in that account.

    :param df: A `DataFrame` of file information, as returned by
        `EndaqCloud.get_file_table()`.
    :return: A `DataFrame` summarizing the tags in `df`.
    """
    # NOTE: Called `tags_count()` in Confluence docs. Function names should
    #   generally be verbs or verb phrases.
    # IDEAS:
    #   * Make this a @classmethod to make EndaqCloud the primary means of access?


def json_table_to_df(data: dict) -> DataFrame:
    """

    :param data:
    :return:
    """
    # IDEAS:
    #   * Make this a @classmethod to make EndaqCloud the primary means of access?
