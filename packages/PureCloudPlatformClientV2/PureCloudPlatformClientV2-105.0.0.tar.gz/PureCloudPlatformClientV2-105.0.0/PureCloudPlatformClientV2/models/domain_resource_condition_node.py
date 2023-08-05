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

class DomainResourceConditionNode(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DomainResourceConditionNode - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'variable_name': 'str',
            'operator': 'str',
            'operands': 'list[DomainResourceConditionValue]',
            'conjunction': 'str',
            'terms': 'list[DomainResourceConditionNode]'
        }

        self.attribute_map = {
            'variable_name': 'variableName',
            'operator': 'operator',
            'operands': 'operands',
            'conjunction': 'conjunction',
            'terms': 'terms'
        }

        self._variable_name = None
        self._operator = None
        self._operands = None
        self._conjunction = None
        self._terms = None

    @property
    def variable_name(self):
        """
        Gets the variable_name of this DomainResourceConditionNode.


        :return: The variable_name of this DomainResourceConditionNode.
        :rtype: str
        """
        return self._variable_name

    @variable_name.setter
    def variable_name(self, variable_name):
        """
        Sets the variable_name of this DomainResourceConditionNode.


        :param variable_name: The variable_name of this DomainResourceConditionNode.
        :type: str
        """
        
        self._variable_name = variable_name

    @property
    def operator(self):
        """
        Gets the operator of this DomainResourceConditionNode.


        :return: The operator of this DomainResourceConditionNode.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """
        Sets the operator of this DomainResourceConditionNode.


        :param operator: The operator of this DomainResourceConditionNode.
        :type: str
        """
        allowed_values = ["EQ", "IN", "GE", "GT", "LE", "LT"]
        if operator.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for operator -> " + operator)
            self._operator = "outdated_sdk_version"
        else:
            self._operator = operator

    @property
    def operands(self):
        """
        Gets the operands of this DomainResourceConditionNode.


        :return: The operands of this DomainResourceConditionNode.
        :rtype: list[DomainResourceConditionValue]
        """
        return self._operands

    @operands.setter
    def operands(self, operands):
        """
        Sets the operands of this DomainResourceConditionNode.


        :param operands: The operands of this DomainResourceConditionNode.
        :type: list[DomainResourceConditionValue]
        """
        
        self._operands = operands

    @property
    def conjunction(self):
        """
        Gets the conjunction of this DomainResourceConditionNode.


        :return: The conjunction of this DomainResourceConditionNode.
        :rtype: str
        """
        return self._conjunction

    @conjunction.setter
    def conjunction(self, conjunction):
        """
        Sets the conjunction of this DomainResourceConditionNode.


        :param conjunction: The conjunction of this DomainResourceConditionNode.
        :type: str
        """
        allowed_values = ["AND", "OR"]
        if conjunction.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for conjunction -> " + conjunction)
            self._conjunction = "outdated_sdk_version"
        else:
            self._conjunction = conjunction

    @property
    def terms(self):
        """
        Gets the terms of this DomainResourceConditionNode.


        :return: The terms of this DomainResourceConditionNode.
        :rtype: list[DomainResourceConditionNode]
        """
        return self._terms

    @terms.setter
    def terms(self, terms):
        """
        Sets the terms of this DomainResourceConditionNode.


        :param terms: The terms of this DomainResourceConditionNode.
        :type: list[DomainResourceConditionNode]
        """
        
        self._terms = terms

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

