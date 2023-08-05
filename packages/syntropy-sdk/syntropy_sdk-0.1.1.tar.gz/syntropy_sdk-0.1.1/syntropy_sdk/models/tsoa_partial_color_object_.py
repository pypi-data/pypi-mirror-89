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


class TsoaPartialColorObject_(object):
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
        "color_id": "float",
        "color_bandwidth": "ConstraintEnum",
        "color_jitter": "ConstraintEnum",
        "color_latency": "ConstraintEnum",
        "color_price": "ConstraintEnum",
    }

    attribute_map = {
        "color_id": "color_id",
        "color_bandwidth": "color_bandwidth",
        "color_jitter": "color_jitter",
        "color_latency": "color_latency",
        "color_price": "color_price",
    }

    def __init__(
        self,
        color_id=None,
        color_bandwidth=None,
        color_jitter=None,
        color_latency=None,
        color_price=None,
    ):  # noqa: E501
        """TsoaPartialColorObject_ - a model defined in Swagger"""  # noqa: E501
        self._color_id = None
        self._color_bandwidth = None
        self._color_jitter = None
        self._color_latency = None
        self._color_price = None
        self.discriminator = None
        if color_id is not None:
            self.color_id = color_id
        if color_bandwidth is not None:
            self.color_bandwidth = color_bandwidth
        if color_jitter is not None:
            self.color_jitter = color_jitter
        if color_latency is not None:
            self.color_latency = color_latency
        if color_price is not None:
            self.color_price = color_price

    @property
    def color_id(self):
        """Gets the color_id of this TsoaPartialColorObject_.  # noqa: E501


        :return: The color_id of this TsoaPartialColorObject_.  # noqa: E501
        :rtype: float
        """
        return self._color_id

    @color_id.setter
    def color_id(self, color_id):
        """Sets the color_id of this TsoaPartialColorObject_.


        :param color_id: The color_id of this TsoaPartialColorObject_.  # noqa: E501
        :type: float
        """

        self._color_id = color_id

    @property
    def color_bandwidth(self):
        """Gets the color_bandwidth of this TsoaPartialColorObject_.  # noqa: E501


        :return: The color_bandwidth of this TsoaPartialColorObject_.  # noqa: E501
        :rtype: ConstraintEnum
        """
        return self._color_bandwidth

    @color_bandwidth.setter
    def color_bandwidth(self, color_bandwidth):
        """Sets the color_bandwidth of this TsoaPartialColorObject_.


        :param color_bandwidth: The color_bandwidth of this TsoaPartialColorObject_.  # noqa: E501
        :type: ConstraintEnum
        """

        self._color_bandwidth = color_bandwidth

    @property
    def color_jitter(self):
        """Gets the color_jitter of this TsoaPartialColorObject_.  # noqa: E501


        :return: The color_jitter of this TsoaPartialColorObject_.  # noqa: E501
        :rtype: ConstraintEnum
        """
        return self._color_jitter

    @color_jitter.setter
    def color_jitter(self, color_jitter):
        """Sets the color_jitter of this TsoaPartialColorObject_.


        :param color_jitter: The color_jitter of this TsoaPartialColorObject_.  # noqa: E501
        :type: ConstraintEnum
        """

        self._color_jitter = color_jitter

    @property
    def color_latency(self):
        """Gets the color_latency of this TsoaPartialColorObject_.  # noqa: E501


        :return: The color_latency of this TsoaPartialColorObject_.  # noqa: E501
        :rtype: ConstraintEnum
        """
        return self._color_latency

    @color_latency.setter
    def color_latency(self, color_latency):
        """Sets the color_latency of this TsoaPartialColorObject_.


        :param color_latency: The color_latency of this TsoaPartialColorObject_.  # noqa: E501
        :type: ConstraintEnum
        """

        self._color_latency = color_latency

    @property
    def color_price(self):
        """Gets the color_price of this TsoaPartialColorObject_.  # noqa: E501


        :return: The color_price of this TsoaPartialColorObject_.  # noqa: E501
        :rtype: ConstraintEnum
        """
        return self._color_price

    @color_price.setter
    def color_price(self, color_price):
        """Sets the color_price of this TsoaPartialColorObject_.


        :param color_price: The color_price of this TsoaPartialColorObject_.  # noqa: E501
        :type: ConstraintEnum
        """

        self._color_price = color_price

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
        if issubclass(TsoaPartialColorObject_, dict):
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
        if not isinstance(other, TsoaPartialColorObject_):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
