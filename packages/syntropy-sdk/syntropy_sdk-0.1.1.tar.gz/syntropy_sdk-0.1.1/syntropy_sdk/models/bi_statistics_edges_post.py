# coding: utf-8

"""
    syntropy-controller

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class BiStatisticsEdgesPost(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "time_window": "float",
        "successful_requests_count": "float",
        "erroneous_requests_count": "float",
        "requests_count": "float",
        "pending_requests_count": "float",
    }

    attribute_map = {
        "time_window": "timeWindow",
        "successful_requests_count": "successfulRequestsCount",
        "erroneous_requests_count": "erroneousRequestsCount",
        "requests_count": "requestsCount",
        "pending_requests_count": "pendingRequestsCount",
    }

    def __init__(
        self,
        time_window=None,
        successful_requests_count=None,
        erroneous_requests_count=None,
        requests_count=None,
        pending_requests_count=None,
    ):  # noqa: E501
        """BiStatisticsEdgesPost - a model defined in Swagger"""  # noqa: E501
        self._time_window = None
        self._successful_requests_count = None
        self._erroneous_requests_count = None
        self._requests_count = None
        self._pending_requests_count = None
        self.discriminator = None
        self.time_window = time_window
        self.successful_requests_count = successful_requests_count
        self.erroneous_requests_count = erroneous_requests_count
        self.requests_count = requests_count
        self.pending_requests_count = pending_requests_count

    @property
    def time_window(self):
        """Gets the time_window of this BiStatisticsEdgesPost.  # noqa: E501


        :return: The time_window of this BiStatisticsEdgesPost.  # noqa: E501
        :rtype: float
        """
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        """Sets the time_window of this BiStatisticsEdgesPost.


        :param time_window: The time_window of this BiStatisticsEdgesPost.  # noqa: E501
        :type: float
        """
        if time_window is None:
            raise ValueError(
                "Invalid value for `time_window`, must not be `None`"
            )  # noqa: E501

        self._time_window = time_window

    @property
    def successful_requests_count(self):
        """Gets the successful_requests_count of this BiStatisticsEdgesPost.  # noqa: E501


        :return: The successful_requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :rtype: float
        """
        return self._successful_requests_count

    @successful_requests_count.setter
    def successful_requests_count(self, successful_requests_count):
        """Sets the successful_requests_count of this BiStatisticsEdgesPost.


        :param successful_requests_count: The successful_requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :type: float
        """
        if successful_requests_count is None:
            raise ValueError(
                "Invalid value for `successful_requests_count`, must not be `None`"
            )  # noqa: E501

        self._successful_requests_count = successful_requests_count

    @property
    def erroneous_requests_count(self):
        """Gets the erroneous_requests_count of this BiStatisticsEdgesPost.  # noqa: E501


        :return: The erroneous_requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :rtype: float
        """
        return self._erroneous_requests_count

    @erroneous_requests_count.setter
    def erroneous_requests_count(self, erroneous_requests_count):
        """Sets the erroneous_requests_count of this BiStatisticsEdgesPost.


        :param erroneous_requests_count: The erroneous_requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :type: float
        """
        if erroneous_requests_count is None:
            raise ValueError(
                "Invalid value for `erroneous_requests_count`, must not be `None`"
            )  # noqa: E501

        self._erroneous_requests_count = erroneous_requests_count

    @property
    def requests_count(self):
        """Gets the requests_count of this BiStatisticsEdgesPost.  # noqa: E501


        :return: The requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :rtype: float
        """
        return self._requests_count

    @requests_count.setter
    def requests_count(self, requests_count):
        """Sets the requests_count of this BiStatisticsEdgesPost.


        :param requests_count: The requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :type: float
        """
        if requests_count is None:
            raise ValueError(
                "Invalid value for `requests_count`, must not be `None`"
            )  # noqa: E501

        self._requests_count = requests_count

    @property
    def pending_requests_count(self):
        """Gets the pending_requests_count of this BiStatisticsEdgesPost.  # noqa: E501


        :return: The pending_requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :rtype: float
        """
        return self._pending_requests_count

    @pending_requests_count.setter
    def pending_requests_count(self, pending_requests_count):
        """Sets the pending_requests_count of this BiStatisticsEdgesPost.


        :param pending_requests_count: The pending_requests_count of this BiStatisticsEdgesPost.  # noqa: E501
        :type: float
        """
        if pending_requests_count is None:
            raise ValueError(
                "Invalid value for `pending_requests_count`, must not be `None`"
            )  # noqa: E501

        self._pending_requests_count = pending_requests_count

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(BiStatisticsEdgesPost, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BiStatisticsEdgesPost):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
