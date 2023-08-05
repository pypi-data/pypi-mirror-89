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

class ScimV2EnterpriseUser(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ScimV2EnterpriseUser - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'division': 'str',
            'department': 'str',
            'manager': 'Manager',
            'employee_number': 'str'
        }

        self.attribute_map = {
            'division': 'division',
            'department': 'department',
            'manager': 'manager',
            'employee_number': 'employeeNumber'
        }

        self._division = None
        self._department = None
        self._manager = None
        self._employee_number = None

    @property
    def division(self):
        """
        Gets the division of this ScimV2EnterpriseUser.
        The division that the user belongs to.

        :return: The division of this ScimV2EnterpriseUser.
        :rtype: str
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this ScimV2EnterpriseUser.
        The division that the user belongs to.

        :param division: The division of this ScimV2EnterpriseUser.
        :type: str
        """
        
        self._division = division

    @property
    def department(self):
        """
        Gets the department of this ScimV2EnterpriseUser.
        The department that the user belongs to.

        :return: The department of this ScimV2EnterpriseUser.
        :rtype: str
        """
        return self._department

    @department.setter
    def department(self, department):
        """
        Sets the department of this ScimV2EnterpriseUser.
        The department that the user belongs to.

        :param department: The department of this ScimV2EnterpriseUser.
        :type: str
        """
        
        self._department = department

    @property
    def manager(self):
        """
        Gets the manager of this ScimV2EnterpriseUser.
        The user's manager.

        :return: The manager of this ScimV2EnterpriseUser.
        :rtype: Manager
        """
        return self._manager

    @manager.setter
    def manager(self, manager):
        """
        Sets the manager of this ScimV2EnterpriseUser.
        The user's manager.

        :param manager: The manager of this ScimV2EnterpriseUser.
        :type: Manager
        """
        
        self._manager = manager

    @property
    def employee_number(self):
        """
        Gets the employee_number of this ScimV2EnterpriseUser.
        The user's employee number.

        :return: The employee_number of this ScimV2EnterpriseUser.
        :rtype: str
        """
        return self._employee_number

    @employee_number.setter
    def employee_number(self, employee_number):
        """
        Sets the employee_number of this ScimV2EnterpriseUser.
        The user's employee number.

        :param employee_number: The employee_number of this ScimV2EnterpriseUser.
        :type: str
        """
        
        self._employee_number = employee_number

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

