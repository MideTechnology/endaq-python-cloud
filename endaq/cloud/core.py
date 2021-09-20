"""
Core enDAQ Cloud communication API
"""


class EndaqCloud:
    """

    """

    def __init__(self, api_key=None, env=None, test=True):
        """
        Constructor for an `EndaqCloud` object, which provides access to an
        enDAQ Cloud account.

        :param api_key:
        :param env:
        :param test: If `True` (default), the connection to enDAQ Cloud will
            be tested before being returned. A failed test will generate a
            meaningful error message describing the problem.
        """

    def get_file(self, file_id, localfile=None):
        """

        :param file_id:
        :param localfile:
        :return:
        """


    def get_file_table(self, limit=100, attributes="all"):
        """

        :param limit:
        :param attributes:
        :return:
        """


    def get_devices(self):
        """

        :return:
        """

    def set_attributes(self, file_id, attributes):
        """

        :param file_id:
        :param attributes:
        :return:
        """


