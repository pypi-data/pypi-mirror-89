# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class CreateManagementUnitApiRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CreateManagementUnitApiRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'time_zone': 'str',
            'start_day_of_week': 'str',
            'settings': 'CreateManagementUnitSettingsRequest',
            'division_id': 'str',
            'business_unit_id': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'time_zone': 'timeZone',
            'start_day_of_week': 'startDayOfWeek',
            'settings': 'settings',
            'division_id': 'divisionId',
            'business_unit_id': 'businessUnitId'
        }

        self._name = None
        self._time_zone = None
        self._start_day_of_week = None
        self._settings = None
        self._division_id = None
        self._business_unit_id = None

    @property
    def name(self):
        """
        Gets the name of this CreateManagementUnitApiRequest.
        The name of the management unit

        :return: The name of this CreateManagementUnitApiRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateManagementUnitApiRequest.
        The name of the management unit

        :param name: The name of this CreateManagementUnitApiRequest.
        :type: str
        """
        
        self._name = name

    @property
    def time_zone(self):
        """
        Gets the time_zone of this CreateManagementUnitApiRequest.
        The default time zone to use for this management unit.  Moving to Business Unit

        :return: The time_zone of this CreateManagementUnitApiRequest.
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """
        Sets the time_zone of this CreateManagementUnitApiRequest.
        The default time zone to use for this management unit.  Moving to Business Unit

        :param time_zone: The time_zone of this CreateManagementUnitApiRequest.
        :type: str
        """
        
        self._time_zone = time_zone

    @property
    def start_day_of_week(self):
        """
        Gets the start_day_of_week of this CreateManagementUnitApiRequest.
        The configured first day of the week for scheduling and forecasting purposes. Moving to Business Unit

        :return: The start_day_of_week of this CreateManagementUnitApiRequest.
        :rtype: str
        """
        return self._start_day_of_week

    @start_day_of_week.setter
    def start_day_of_week(self, start_day_of_week):
        """
        Sets the start_day_of_week of this CreateManagementUnitApiRequest.
        The configured first day of the week for scheduling and forecasting purposes. Moving to Business Unit

        :param start_day_of_week: The start_day_of_week of this CreateManagementUnitApiRequest.
        :type: str
        """
        allowed_values = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if start_day_of_week.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for start_day_of_week -> " + start_day_of_week)
            self._start_day_of_week = "outdated_sdk_version"
        else:
            self._start_day_of_week = start_day_of_week

    @property
    def settings(self):
        """
        Gets the settings of this CreateManagementUnitApiRequest.
        The configuration for the management unit.  If omitted, reasonable defaults will be assigned

        :return: The settings of this CreateManagementUnitApiRequest.
        :rtype: CreateManagementUnitSettingsRequest
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """
        Sets the settings of this CreateManagementUnitApiRequest.
        The configuration for the management unit.  If omitted, reasonable defaults will be assigned

        :param settings: The settings of this CreateManagementUnitApiRequest.
        :type: CreateManagementUnitSettingsRequest
        """
        
        self._settings = settings

    @property
    def division_id(self):
        """
        Gets the division_id of this CreateManagementUnitApiRequest.
        The id of the division to which this management unit belongs.  Defaults to home division ID

        :return: The division_id of this CreateManagementUnitApiRequest.
        :rtype: str
        """
        return self._division_id

    @division_id.setter
    def division_id(self, division_id):
        """
        Sets the division_id of this CreateManagementUnitApiRequest.
        The id of the division to which this management unit belongs.  Defaults to home division ID

        :param division_id: The division_id of this CreateManagementUnitApiRequest.
        :type: str
        """
        
        self._division_id = division_id

    @property
    def business_unit_id(self):
        """
        Gets the business_unit_id of this CreateManagementUnitApiRequest.
        The id of the business unit to which this management unit belongs.  Required after business unit launch

        :return: The business_unit_id of this CreateManagementUnitApiRequest.
        :rtype: str
        """
        return self._business_unit_id

    @business_unit_id.setter
    def business_unit_id(self, business_unit_id):
        """
        Sets the business_unit_id of this CreateManagementUnitApiRequest.
        The id of the business unit to which this management unit belongs.  Required after business unit launch

        :param business_unit_id: The business_unit_id of this CreateManagementUnitApiRequest.
        :type: str
        """
        
        self._business_unit_id = business_unit_id

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

