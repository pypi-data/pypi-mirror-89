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


class TsoaPartialRouteObject_(object):
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
        "server_vin_id": "float",
        "server_ven_id": "float",
        "route_bandwidth": "float",
        "route_price": "float",
        "route_jitter": "float",
        "route_latency": "float",
        "route_status": "Status",
        "route_status_reason": "str",
    }

    attribute_map = {
        "server_vin_id": "server_vin_id",
        "server_ven_id": "server_ven_id",
        "route_bandwidth": "route_bandwidth",
        "route_price": "route_price",
        "route_jitter": "route_jitter",
        "route_latency": "route_latency",
        "route_status": "route_status",
        "route_status_reason": "route_status_reason",
    }

    def __init__(
        self,
        server_vin_id=None,
        server_ven_id=None,
        route_bandwidth=None,
        route_price=None,
        route_jitter=None,
        route_latency=None,
        route_status=None,
        route_status_reason=None,
    ):  # noqa: E501
        """TsoaPartialRouteObject_ - a model defined in Swagger"""  # noqa: E501
        self._server_vin_id = None
        self._server_ven_id = None
        self._route_bandwidth = None
        self._route_price = None
        self._route_jitter = None
        self._route_latency = None
        self._route_status = None
        self._route_status_reason = None
        self.discriminator = None
        if server_vin_id is not None:
            self.server_vin_id = server_vin_id
        if server_ven_id is not None:
            self.server_ven_id = server_ven_id
        if route_bandwidth is not None:
            self.route_bandwidth = route_bandwidth
        if route_price is not None:
            self.route_price = route_price
        if route_jitter is not None:
            self.route_jitter = route_jitter
        if route_latency is not None:
            self.route_latency = route_latency
        if route_status is not None:
            self.route_status = route_status
        if route_status_reason is not None:
            self.route_status_reason = route_status_reason

    @property
    def server_vin_id(self):
        """Gets the server_vin_id of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The server_vin_id of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: float
        """
        return self._server_vin_id

    @server_vin_id.setter
    def server_vin_id(self, server_vin_id):
        """Sets the server_vin_id of this TsoaPartialRouteObject_.


        :param server_vin_id: The server_vin_id of this TsoaPartialRouteObject_.  # noqa: E501
        :type: float
        """

        self._server_vin_id = server_vin_id

    @property
    def server_ven_id(self):
        """Gets the server_ven_id of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The server_ven_id of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: float
        """
        return self._server_ven_id

    @server_ven_id.setter
    def server_ven_id(self, server_ven_id):
        """Sets the server_ven_id of this TsoaPartialRouteObject_.


        :param server_ven_id: The server_ven_id of this TsoaPartialRouteObject_.  # noqa: E501
        :type: float
        """

        self._server_ven_id = server_ven_id

    @property
    def route_bandwidth(self):
        """Gets the route_bandwidth of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The route_bandwidth of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: float
        """
        return self._route_bandwidth

    @route_bandwidth.setter
    def route_bandwidth(self, route_bandwidth):
        """Sets the route_bandwidth of this TsoaPartialRouteObject_.


        :param route_bandwidth: The route_bandwidth of this TsoaPartialRouteObject_.  # noqa: E501
        :type: float
        """

        self._route_bandwidth = route_bandwidth

    @property
    def route_price(self):
        """Gets the route_price of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The route_price of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: float
        """
        return self._route_price

    @route_price.setter
    def route_price(self, route_price):
        """Sets the route_price of this TsoaPartialRouteObject_.


        :param route_price: The route_price of this TsoaPartialRouteObject_.  # noqa: E501
        :type: float
        """

        self._route_price = route_price

    @property
    def route_jitter(self):
        """Gets the route_jitter of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The route_jitter of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: float
        """
        return self._route_jitter

    @route_jitter.setter
    def route_jitter(self, route_jitter):
        """Sets the route_jitter of this TsoaPartialRouteObject_.


        :param route_jitter: The route_jitter of this TsoaPartialRouteObject_.  # noqa: E501
        :type: float
        """

        self._route_jitter = route_jitter

    @property
    def route_latency(self):
        """Gets the route_latency of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The route_latency of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: float
        """
        return self._route_latency

    @route_latency.setter
    def route_latency(self, route_latency):
        """Sets the route_latency of this TsoaPartialRouteObject_.


        :param route_latency: The route_latency of this TsoaPartialRouteObject_.  # noqa: E501
        :type: float
        """

        self._route_latency = route_latency

    @property
    def route_status(self):
        """Gets the route_status of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The route_status of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: Status
        """
        return self._route_status

    @route_status.setter
    def route_status(self, route_status):
        """Sets the route_status of this TsoaPartialRouteObject_.


        :param route_status: The route_status of this TsoaPartialRouteObject_.  # noqa: E501
        :type: Status
        """

        self._route_status = route_status

    @property
    def route_status_reason(self):
        """Gets the route_status_reason of this TsoaPartialRouteObject_.  # noqa: E501


        :return: The route_status_reason of this TsoaPartialRouteObject_.  # noqa: E501
        :rtype: str
        """
        return self._route_status_reason

    @route_status_reason.setter
    def route_status_reason(self, route_status_reason):
        """Sets the route_status_reason of this TsoaPartialRouteObject_.


        :param route_status_reason: The route_status_reason of this TsoaPartialRouteObject_.  # noqa: E501
        :type: str
        """

        self._route_status_reason = route_status_reason

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
        if issubclass(TsoaPartialRouteObject_, dict):
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
        if not isinstance(other, TsoaPartialRouteObject_):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
