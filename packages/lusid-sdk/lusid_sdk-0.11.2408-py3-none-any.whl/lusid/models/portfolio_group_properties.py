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

class PortfolioGroupProperties(object):
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
        'href': 'str',
        'properties': 'dict(str, ModelProperty)',
        'version': 'Version',
        'links': 'list[Link]'
    }

    attribute_map = {
        'href': 'href',
        'properties': 'properties',
        'version': 'version',
        'links': 'links'
    }

    required_map = {
        'href': 'optional',
        'properties': 'optional',
        'version': 'optional',
        'links': 'optional'
    }

    def __init__(self, href=None, properties=None, version=None, links=None):  # noqa: E501
        """
        PortfolioGroupProperties - a model defined in OpenAPI

        :param href:  The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.
        :type href: str
        :param properties:  The portfolio group properties. These will be from the 'PortfolioGroup' domain.
        :type properties: dict[str, lusid.ModelProperty]
        :param version: 
        :type version: lusid.Version
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501

        self._href = None
        self._properties = None
        self._version = None
        self._links = None
        self.discriminator = None

        self.href = href
        self.properties = properties
        if version is not None:
            self.version = version
        self.links = links

    @property
    def href(self):
        """Gets the href of this PortfolioGroupProperties.  # noqa: E501

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :return: The href of this PortfolioGroupProperties.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this PortfolioGroupProperties.

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :param href: The href of this PortfolioGroupProperties.  # noqa: E501
        :type: str
        """

        self._href = href

    @property
    def properties(self):
        """Gets the properties of this PortfolioGroupProperties.  # noqa: E501

        The portfolio group properties. These will be from the 'PortfolioGroup' domain.  # noqa: E501

        :return: The properties of this PortfolioGroupProperties.  # noqa: E501
        :rtype: dict(str, ModelProperty)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this PortfolioGroupProperties.

        The portfolio group properties. These will be from the 'PortfolioGroup' domain.  # noqa: E501

        :param properties: The properties of this PortfolioGroupProperties.  # noqa: E501
        :type: dict(str, ModelProperty)
        """

        self._properties = properties

    @property
    def version(self):
        """Gets the version of this PortfolioGroupProperties.  # noqa: E501


        :return: The version of this PortfolioGroupProperties.  # noqa: E501
        :rtype: Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this PortfolioGroupProperties.


        :param version: The version of this PortfolioGroupProperties.  # noqa: E501
        :type: Version
        """

        self._version = version

    @property
    def links(self):
        """Gets the links of this PortfolioGroupProperties.  # noqa: E501


        :return: The links of this PortfolioGroupProperties.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this PortfolioGroupProperties.


        :param links: The links of this PortfolioGroupProperties.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

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
        if not isinstance(other, PortfolioGroupProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
