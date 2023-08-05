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

class UpdateCutLabelDefinitionRequest(object):
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
        'display_name': 'str',
        'description': 'str',
        'cut_local_time': 'CutLocalTime',
        'time_zone': 'str'
    }

    attribute_map = {
        'display_name': 'displayName',
        'description': 'description',
        'cut_local_time': 'cutLocalTime',
        'time_zone': 'timeZone'
    }

    required_map = {
        'display_name': 'required',
        'description': 'optional',
        'cut_local_time': 'required',
        'time_zone': 'required'
    }

    def __init__(self, display_name=None, description=None, cut_local_time=None, time_zone=None):  # noqa: E501
        """
        UpdateCutLabelDefinitionRequest - a model defined in OpenAPI

        :param display_name:  (required)
        :type display_name: str
        :param description: 
        :type description: str
        :param cut_local_time:  (required)
        :type cut_local_time: lusid.CutLocalTime
        :param time_zone:  (required)
        :type time_zone: str

        """  # noqa: E501

        self._display_name = None
        self._description = None
        self._cut_local_time = None
        self._time_zone = None
        self.discriminator = None

        self.display_name = display_name
        self.description = description
        self.cut_local_time = cut_local_time
        self.time_zone = time_zone

    @property
    def display_name(self):
        """Gets the display_name of this UpdateCutLabelDefinitionRequest.  # noqa: E501


        :return: The display_name of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this UpdateCutLabelDefinitionRequest.


        :param display_name: The display_name of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :type: str
        """
        if display_name is None:
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this UpdateCutLabelDefinitionRequest.  # noqa: E501


        :return: The description of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateCutLabelDefinitionRequest.


        :param description: The description of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def cut_local_time(self):
        """Gets the cut_local_time of this UpdateCutLabelDefinitionRequest.  # noqa: E501


        :return: The cut_local_time of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :rtype: CutLocalTime
        """
        return self._cut_local_time

    @cut_local_time.setter
    def cut_local_time(self, cut_local_time):
        """Sets the cut_local_time of this UpdateCutLabelDefinitionRequest.


        :param cut_local_time: The cut_local_time of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :type: CutLocalTime
        """
        if cut_local_time is None:
            raise ValueError("Invalid value for `cut_local_time`, must not be `None`")  # noqa: E501

        self._cut_local_time = cut_local_time

    @property
    def time_zone(self):
        """Gets the time_zone of this UpdateCutLabelDefinitionRequest.  # noqa: E501


        :return: The time_zone of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """Sets the time_zone of this UpdateCutLabelDefinitionRequest.


        :param time_zone: The time_zone of this UpdateCutLabelDefinitionRequest.  # noqa: E501
        :type: str
        """
        if time_zone is None:
            raise ValueError("Invalid value for `time_zone`, must not be `None`")  # noqa: E501

        self._time_zone = time_zone

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
        if not isinstance(other, UpdateCutLabelDefinitionRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
