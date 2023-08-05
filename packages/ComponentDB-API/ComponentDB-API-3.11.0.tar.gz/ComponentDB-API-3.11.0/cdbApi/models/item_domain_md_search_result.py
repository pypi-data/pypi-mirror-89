# coding: utf-8

"""
    Component Database API

    The API that provides access to Component Database data.  # noqa: E501

    The version of the OpenAPI document: 3.8.0
    Contact: djarosz@anl.gov
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from cdbApi.configuration import Configuration


class ItemDomainMdSearchResult(object):
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
    """
    openapi_types = {
        'object_id': 'int',
        'object_name': 'str',
        'object_attribute_match_map': 'dict(str, str)',
        'machine_design': 'ItemDomainMachineDesign',
        'child_items': 'list[ItemDomainMdSearchResult]',
        'search_match': 'bool',
        'display': 'str',
        'empty': 'bool'
    }

    attribute_map = {
        'object_id': 'objectId',
        'object_name': 'objectName',
        'object_attribute_match_map': 'objectAttributeMatchMap',
        'machine_design': 'machineDesign',
        'child_items': 'childItems',
        'search_match': 'searchMatch',
        'display': 'display',
        'empty': 'empty'
    }

    def __init__(self, object_id=None, object_name=None, object_attribute_match_map=None, machine_design=None, child_items=None, search_match=None, display=None, empty=None, local_vars_configuration=None):  # noqa: E501
        """ItemDomainMdSearchResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._object_id = None
        self._object_name = None
        self._object_attribute_match_map = None
        self._machine_design = None
        self._child_items = None
        self._search_match = None
        self._display = None
        self._empty = None
        self.discriminator = None

        if object_id is not None:
            self.object_id = object_id
        if object_name is not None:
            self.object_name = object_name
        if object_attribute_match_map is not None:
            self.object_attribute_match_map = object_attribute_match_map
        if machine_design is not None:
            self.machine_design = machine_design
        if child_items is not None:
            self.child_items = child_items
        if search_match is not None:
            self.search_match = search_match
        if display is not None:
            self.display = display
        if empty is not None:
            self.empty = empty

    @property
    def object_id(self):
        """Gets the object_id of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The object_id of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: int
        """
        return self._object_id

    @object_id.setter
    def object_id(self, object_id):
        """Sets the object_id of this ItemDomainMdSearchResult.


        :param object_id: The object_id of this ItemDomainMdSearchResult.  # noqa: E501
        :type: int
        """

        self._object_id = object_id

    @property
    def object_name(self):
        """Gets the object_name of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The object_name of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._object_name

    @object_name.setter
    def object_name(self, object_name):
        """Sets the object_name of this ItemDomainMdSearchResult.


        :param object_name: The object_name of this ItemDomainMdSearchResult.  # noqa: E501
        :type: str
        """

        self._object_name = object_name

    @property
    def object_attribute_match_map(self):
        """Gets the object_attribute_match_map of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The object_attribute_match_map of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._object_attribute_match_map

    @object_attribute_match_map.setter
    def object_attribute_match_map(self, object_attribute_match_map):
        """Sets the object_attribute_match_map of this ItemDomainMdSearchResult.


        :param object_attribute_match_map: The object_attribute_match_map of this ItemDomainMdSearchResult.  # noqa: E501
        :type: dict(str, str)
        """

        self._object_attribute_match_map = object_attribute_match_map

    @property
    def machine_design(self):
        """Gets the machine_design of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The machine_design of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: ItemDomainMachineDesign
        """
        return self._machine_design

    @machine_design.setter
    def machine_design(self, machine_design):
        """Sets the machine_design of this ItemDomainMdSearchResult.


        :param machine_design: The machine_design of this ItemDomainMdSearchResult.  # noqa: E501
        :type: ItemDomainMachineDesign
        """

        self._machine_design = machine_design

    @property
    def child_items(self):
        """Gets the child_items of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The child_items of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: list[ItemDomainMdSearchResult]
        """
        return self._child_items

    @child_items.setter
    def child_items(self, child_items):
        """Sets the child_items of this ItemDomainMdSearchResult.


        :param child_items: The child_items of this ItemDomainMdSearchResult.  # noqa: E501
        :type: list[ItemDomainMdSearchResult]
        """

        self._child_items = child_items

    @property
    def search_match(self):
        """Gets the search_match of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The search_match of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: bool
        """
        return self._search_match

    @search_match.setter
    def search_match(self, search_match):
        """Sets the search_match of this ItemDomainMdSearchResult.


        :param search_match: The search_match of this ItemDomainMdSearchResult.  # noqa: E501
        :type: bool
        """

        self._search_match = search_match

    @property
    def display(self):
        """Gets the display of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The display of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """Sets the display of this ItemDomainMdSearchResult.


        :param display: The display of this ItemDomainMdSearchResult.  # noqa: E501
        :type: str
        """

        self._display = display

    @property
    def empty(self):
        """Gets the empty of this ItemDomainMdSearchResult.  # noqa: E501


        :return: The empty of this ItemDomainMdSearchResult.  # noqa: E501
        :rtype: bool
        """
        return self._empty

    @empty.setter
    def empty(self, empty):
        """Sets the empty of this ItemDomainMdSearchResult.


        :param empty: The empty of this ItemDomainMdSearchResult.  # noqa: E501
        :type: bool
        """

        self._empty = empty

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
        if not isinstance(other, ItemDomainMdSearchResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ItemDomainMdSearchResult):
            return True

        return self.to_dict() != other.to_dict()
