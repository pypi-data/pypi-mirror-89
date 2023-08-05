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

class CreatePortfolioGroupRequest(object):
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
        'code': 'str',
        'created': 'datetime',
        'values': 'list[ResourceId]',
        'sub_groups': 'list[ResourceId]',
        'properties': 'dict(str, ModelProperty)',
        'display_name': 'str',
        'description': 'str'
    }

    attribute_map = {
        'code': 'code',
        'created': 'created',
        'values': 'values',
        'sub_groups': 'subGroups',
        'properties': 'properties',
        'display_name': 'displayName',
        'description': 'description'
    }

    required_map = {
        'code': 'required',
        'created': 'optional',
        'values': 'optional',
        'sub_groups': 'optional',
        'properties': 'optional',
        'display_name': 'required',
        'description': 'optional'
    }

    def __init__(self, code=None, created=None, values=None, sub_groups=None, properties=None, display_name=None, description=None):  # noqa: E501
        """
        CreatePortfolioGroupRequest - a model defined in OpenAPI

        :param code:  The code that the portfolio group will be created with. Together with the scope this uniquely identifies the portfolio group. (required)
        :type code: str
        :param created:  The effective datetime at which the portfolio group was created. Defaults to the current LUSID system datetime if not specified.
        :type created: datetime
        :param values:  The resource identifiers of the portfolios to be contained within the portfolio group.
        :type values: list[lusid.ResourceId]
        :param sub_groups:  The resource identifiers of the portfolio groups to be contained within the portfolio group as sub groups.
        :type sub_groups: list[lusid.ResourceId]
        :param properties:  A set of unique group properties to add to the portfolio group. Each property must be from the 'PortfolioGroup' domain and should be identified by its key which has the format {domain}/{scope}/{code}, e.g. 'PortfolioGroup/Manager/Id'. These properties must be pre-defined.
        :type properties: dict[str, lusid.ModelProperty]
        :param display_name:  The name of the portfolio group. (required)
        :type display_name: str
        :param description:  A long form description of the portfolio group.
        :type description: str

        """  # noqa: E501

        self._code = None
        self._created = None
        self._values = None
        self._sub_groups = None
        self._properties = None
        self._display_name = None
        self._description = None
        self.discriminator = None

        self.code = code
        self.created = created
        self.values = values
        self.sub_groups = sub_groups
        self.properties = properties
        self.display_name = display_name
        self.description = description

    @property
    def code(self):
        """Gets the code of this CreatePortfolioGroupRequest.  # noqa: E501

        The code that the portfolio group will be created with. Together with the scope this uniquely identifies the portfolio group.  # noqa: E501

        :return: The code of this CreatePortfolioGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this CreatePortfolioGroupRequest.

        The code that the portfolio group will be created with. Together with the scope this uniquely identifies the portfolio group.  # noqa: E501

        :param code: The code of this CreatePortfolioGroupRequest.  # noqa: E501
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

    @property
    def created(self):
        """Gets the created of this CreatePortfolioGroupRequest.  # noqa: E501

        The effective datetime at which the portfolio group was created. Defaults to the current LUSID system datetime if not specified.  # noqa: E501

        :return: The created of this CreatePortfolioGroupRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this CreatePortfolioGroupRequest.

        The effective datetime at which the portfolio group was created. Defaults to the current LUSID system datetime if not specified.  # noqa: E501

        :param created: The created of this CreatePortfolioGroupRequest.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def values(self):
        """Gets the values of this CreatePortfolioGroupRequest.  # noqa: E501

        The resource identifiers of the portfolios to be contained within the portfolio group.  # noqa: E501

        :return: The values of this CreatePortfolioGroupRequest.  # noqa: E501
        :rtype: list[ResourceId]
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this CreatePortfolioGroupRequest.

        The resource identifiers of the portfolios to be contained within the portfolio group.  # noqa: E501

        :param values: The values of this CreatePortfolioGroupRequest.  # noqa: E501
        :type: list[ResourceId]
        """

        self._values = values

    @property
    def sub_groups(self):
        """Gets the sub_groups of this CreatePortfolioGroupRequest.  # noqa: E501

        The resource identifiers of the portfolio groups to be contained within the portfolio group as sub groups.  # noqa: E501

        :return: The sub_groups of this CreatePortfolioGroupRequest.  # noqa: E501
        :rtype: list[ResourceId]
        """
        return self._sub_groups

    @sub_groups.setter
    def sub_groups(self, sub_groups):
        """Sets the sub_groups of this CreatePortfolioGroupRequest.

        The resource identifiers of the portfolio groups to be contained within the portfolio group as sub groups.  # noqa: E501

        :param sub_groups: The sub_groups of this CreatePortfolioGroupRequest.  # noqa: E501
        :type: list[ResourceId]
        """

        self._sub_groups = sub_groups

    @property
    def properties(self):
        """Gets the properties of this CreatePortfolioGroupRequest.  # noqa: E501

        A set of unique group properties to add to the portfolio group. Each property must be from the 'PortfolioGroup' domain and should be identified by its key which has the format {domain}/{scope}/{code}, e.g. 'PortfolioGroup/Manager/Id'. These properties must be pre-defined.  # noqa: E501

        :return: The properties of this CreatePortfolioGroupRequest.  # noqa: E501
        :rtype: dict(str, ModelProperty)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this CreatePortfolioGroupRequest.

        A set of unique group properties to add to the portfolio group. Each property must be from the 'PortfolioGroup' domain and should be identified by its key which has the format {domain}/{scope}/{code}, e.g. 'PortfolioGroup/Manager/Id'. These properties must be pre-defined.  # noqa: E501

        :param properties: The properties of this CreatePortfolioGroupRequest.  # noqa: E501
        :type: dict(str, ModelProperty)
        """

        self._properties = properties

    @property
    def display_name(self):
        """Gets the display_name of this CreatePortfolioGroupRequest.  # noqa: E501

        The name of the portfolio group.  # noqa: E501

        :return: The display_name of this CreatePortfolioGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this CreatePortfolioGroupRequest.

        The name of the portfolio group.  # noqa: E501

        :param display_name: The display_name of this CreatePortfolioGroupRequest.  # noqa: E501
        :type: str
        """
        if display_name is None:
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this CreatePortfolioGroupRequest.  # noqa: E501

        A long form description of the portfolio group.  # noqa: E501

        :return: The description of this CreatePortfolioGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreatePortfolioGroupRequest.

        A long form description of the portfolio group.  # noqa: E501

        :param description: The description of this CreatePortfolioGroupRequest.  # noqa: E501
        :type: str
        """

        self._description = description

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
        if not isinstance(other, CreatePortfolioGroupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
