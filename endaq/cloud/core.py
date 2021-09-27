"""
Core enDAQ Cloud communication API

TODO: Rewrite docstrings (pref. before implementing methods)
"""
from datetime import datetime, timedelta
from typing import Optional, Union

from idelib.dataset import Dataset
import numpy as np
from pandas import DataFrame
import pandas as pd
import requests

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
        self.api_key = api_key
        self.domain = env or ENV_PRODUCTION

        self._account_id = self._account_email = None
        if test:
            info = self.get_account_info()
            if not info.get('id') or not info.get('email'):
                # TODO: change this exception; it's placeholder.
                raise RuntimeError("Failed to connect to enDAQ Cloud: response was {!r}".format(info))


    def get_account_info(self) -> dict:
        """
        Get information about the connected account. Sets or updates the
        values of `account_id` and `account_email`.

        :return: If successful, a dictionary containing (at minimum) the keys
            `email` and `id`.
        """
        response = requests.get(self.domain + "/api/v1/account/info",
                                headers={"x-api-key": self.api_key}).json()
        # Cache the ID and email. Don't clobber if the request failed
        # (just in case - it's unlikely).
        self._account_id = response.get('id', self._account_id)
        self._account_email = response.get('email', self._account_email)
        return response


    @property
    def account_id(self) -> Union[str, None]:
        """ The enDAQ Cloud account's unique ID. """
        if self._account_id is None:
            self.get_account_info()
        return self._account_id


    @property
    def account_email(self) -> Union[str, None]:
        """ The email address associated with the enDAQ Cloud account. """
        if self._account_email is None:
            self.get_account_info()
        return self._account_email


    def get_file(self,
                 file_id: Union[int, str],
                 local_name: Optional[str] = None) -> Dataset:
        """
        Download the specified file to local_name if provided, use the file
        name from the cloud if no local name is provided.
        TODO: This should be made to match `endaq.ide.get_doc()`

        :param file_id: The file's cloud ID.
        :param local_name:
        :return: The imported file, as an `idelib.Dataset`.
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
        # NOTE: Use `json_table_to_df()`
        # THIS IS MOSTLY COLLAB EXAMPLE CODE; NOT FULLY CONVERTED

        if isinstance(attributes, str):
            attributes = attributes.split(',')
        attributes = [str(a).strip() for a in attributes]
        params = {'limit': limit, 'attributes': attributes}
        response = requests.get(self.domain + "/api/v1/files",
                                params=params,
                                headers={"x-api-key": self.api_key})

        df = DataFrame(response.json()['data'])

        # Pull Out Attributes Into Dedicated Columns
        attributes = pd.DataFrame()
        for i in range(len(df)):
            atts = pd.json_normalize(df.attributes.iloc[i]).set_index('name').T.drop(['id', 'type'])
            atts.loc[i] = atts.loc['value']
            attributes = pd.concat([attributes, atts.loc[i]], axis=1)
        df = pd.concat([df, attributes.T], axis=1)

        # Separate GPS
        locs = df['gpsLocationFull'].str.split(',', 1).to_list()
        df['Lat'] = np.nan
        df['Lon'] = np.nan
        for i in range(len(locs)):
            if isinstance(locs[i], list):
                df.loc[i, 'Lat'] = float(locs[i][0])
                df.loc[i, 'Lon'] = float(locs[i][1])

        # Change type to float for our attribute columns of interest,
        # Note that this can be done using the type from the attributes in the API response... too lazy
        att_cols = ['gyroscopeRMSFull', 'gpsSpeedFull',
                    'accelerationPeakFull', 'velocityRMSFull', 'psuedoVelocityPeakFull',
                    'temperatureMeanFull', 'accelerationRMSFull', 'microphonoeRMSFull',
                    'pressureMeanFull', 'accelerometerSampleRateFull', 'displacementRMSFull']
        for c in att_cols:
            df[c] = df[c].astype(float)

        # Add Human Readable Datetime Stamps
        df['Date Recorded'] = pd.to_datetime(df['recording_ts'], unit='s') - timedelta(hours=4)
        df['Date Uploaded'] = pd.to_datetime(df['created_ts'], unit='s') - timedelta(hours=4)
        df['Date Modified'] = pd.to_datetime(df['modified_ts'], unit='s') - timedelta(hours=4)

        return df


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
    Convert JSON parsed from a custom report to a more user-friendly
    `pandas.DataFrame`.

    :param data: A `dict` of data from a custom report's JSON.
    :return: A formatted `DataFrame`
    """
    # NOTE: Steve wanted this as a separate function.
    #  Also: is this already implemented as `endaq.cloud.utilities.convert_file_data_to_dataframe()`?
    # IDEAS:
    #   * Make this a @classmethod to make EndaqCloud class and/or instances the primary means of access?
