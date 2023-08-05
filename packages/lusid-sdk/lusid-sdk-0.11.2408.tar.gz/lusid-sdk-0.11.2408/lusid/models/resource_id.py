# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.2408
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class ResourceId(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'scope': 'str',
        'code': 'str'
    }

    attribute_map = {
        'scope': 'scope',
        'code': 'code'
    }

    required_map = {
        'scope': 'optional',
        'code': 'optional'
    }

    def __init__(self, scope=None, code=None):  # noqa: E501
        """
        ResourceId - a model defined in OpenAPI

        :param scope: 
        :type scope: str
        :param code: 
        :type code: str

        """  # noqa: E501

        self._scope = None
        self._code = None
        self.discriminator = None

        self.scope = scope
        self.code = code

    @property
    def scope(self):
        """Gets the scope of this ResourceId.  # noqa: E501


        :return: The scope of this ResourceId.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this ResourceId.


        :param scope: The scope of this ResourceId.  # noqa: E501
        :type: str
        """

        self._scope = scope

    @property
    def code(self):
        """Gets the code of this ResourceId.  # noqa: E501


        :return: The code of this ResourceId.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this ResourceId.


        :param code: The code of this ResourceId.  # noqa: E501
        :type: str
        """

        self._code = code

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ResourceId):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
