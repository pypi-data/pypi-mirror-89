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


class VppCallableObjectArgs7(object):
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
        "endpoints": "list[str]",
        "port": "float",
        "addr": "str",
        "ifname": "str",
    }

    attribute_map = {
        "endpoints": "endpoints",
        "port": "port",
        "addr": "addr",
        "ifname": "ifname",
    }

    def __init__(self, endpoints=None, port=None, addr=None, ifname=None):  # noqa: E501
        """VppCallableObjectArgs7 - a model defined in Swagger"""  # noqa: E501
        self._endpoints = None
        self._port = None
        self._addr = None
        self._ifname = None
        self.discriminator = None
        self.endpoints = endpoints
        self.port = port
        if addr is not None:
            self.addr = addr
        self.ifname = ifname

    @property
    def endpoints(self):
        """Gets the endpoints of this VppCallableObjectArgs7.  # noqa: E501


        :return: The endpoints of this VppCallableObjectArgs7.  # noqa: E501
        :rtype: list[str]
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints):
        """Sets the endpoints of this VppCallableObjectArgs7.


        :param endpoints: The endpoints of this VppCallableObjectArgs7.  # noqa: E501
        :type: list[str]
        """
        if endpoints is None:
            raise ValueError(
                "Invalid value for `endpoints`, must not be `None`"
            )  # noqa: E501

        self._endpoints = endpoints

    @property
    def port(self):
        """Gets the port of this VppCallableObjectArgs7.  # noqa: E501


        :return: The port of this VppCallableObjectArgs7.  # noqa: E501
        :rtype: float
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this VppCallableObjectArgs7.


        :param port: The port of this VppCallableObjectArgs7.  # noqa: E501
        :type: float
        """
        if port is None:
            raise ValueError(
                "Invalid value for `port`, must not be `None`"
            )  # noqa: E501

        self._port = port

    @property
    def addr(self):
        """Gets the addr of this VppCallableObjectArgs7.  # noqa: E501


        :return: The addr of this VppCallableObjectArgs7.  # noqa: E501
        :rtype: str
        """
        return self._addr

    @addr.setter
    def addr(self, addr):
        """Sets the addr of this VppCallableObjectArgs7.


        :param addr: The addr of this VppCallableObjectArgs7.  # noqa: E501
        :type: str
        """

        self._addr = addr

    @property
    def ifname(self):
        """Gets the ifname of this VppCallableObjectArgs7.  # noqa: E501


        :return: The ifname of this VppCallableObjectArgs7.  # noqa: E501
        :rtype: str
        """
        return self._ifname

    @ifname.setter
    def ifname(self, ifname):
        """Sets the ifname of this VppCallableObjectArgs7.


        :param ifname: The ifname of this VppCallableObjectArgs7.  # noqa: E501
        :type: str
        """
        if ifname is None:
            raise ValueError(
                "Invalid value for `ifname`, must not be `None`"
            )  # noqa: E501

        self._ifname = ifname

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
        if issubclass(VppCallableObjectArgs7, dict):
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
        if not isinstance(other, VppCallableObjectArgs7):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
