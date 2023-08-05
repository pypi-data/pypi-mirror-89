# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.2407
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class UpsertQuoteAccessMetadataRuleRequest(object):
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
        'id': 'QuoteAccessMetadataRuleId',
        'metadata': 'dict(str, list[AccessMetadataValue])'
    }

    attribute_map = {
        'id': 'id',
        'metadata': 'metadata'
    }

    required_map = {
        'id': 'required',
        'metadata': 'required'
    }

    def __init__(self, id=None, metadata=None):  # noqa: E501
        """
        UpsertQuoteAccessMetadataRuleRequest - a model defined in OpenAPI

        :param id:  (required)
        :type id: lusid.QuoteAccessMetadataRuleId
        :param metadata:  The access control metadata to assign to quotes that match the identifier (required)
        :type metadata: dict(str, list[AccessMetadataValue])

        """  # noqa: E501

        self._id = None
        self._metadata = None
        self.discriminator = None

        self.id = id
        self.metadata = metadata

    @property
    def id(self):
        """Gets the id of this UpsertQuoteAccessMetadataRuleRequest.  # noqa: E501


        :return: The id of this UpsertQuoteAccessMetadataRuleRequest.  # noqa: E501
        :rtype: QuoteAccessMetadataRuleId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UpsertQuoteAccessMetadataRuleRequest.


        :param id: The id of this UpsertQuoteAccessMetadataRuleRequest.  # noqa: E501
        :type: QuoteAccessMetadataRuleId
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def metadata(self):
        """Gets the metadata of this UpsertQuoteAccessMetadataRuleRequest.  # noqa: E501

        The access control metadata to assign to quotes that match the identifier  # noqa: E501

        :return: The metadata of this UpsertQuoteAccessMetadataRuleRequest.  # noqa: E501
        :rtype: dict(str, list[AccessMetadataValue])
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this UpsertQuoteAccessMetadataRuleRequest.

        The access control metadata to assign to quotes that match the identifier  # noqa: E501

        :param metadata: The metadata of this UpsertQuoteAccessMetadataRuleRequest.  # noqa: E501
        :type: dict(str, list[AccessMetadataValue])
        """
        if metadata is None:
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

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
        if not isinstance(other, UpsertQuoteAccessMetadataRuleRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
