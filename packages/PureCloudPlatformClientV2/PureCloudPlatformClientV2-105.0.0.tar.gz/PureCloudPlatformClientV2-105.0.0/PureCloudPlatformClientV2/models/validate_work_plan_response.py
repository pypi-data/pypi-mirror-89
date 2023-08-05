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

class ValidateWorkPlanResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ValidateWorkPlanResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'work_plan': 'WorkPlanReference',
            'valid': 'bool',
            'messages': 'ValidateWorkPlanMessages'
        }

        self.attribute_map = {
            'work_plan': 'workPlan',
            'valid': 'valid',
            'messages': 'messages'
        }

        self._work_plan = None
        self._valid = None
        self._messages = None

    @property
    def work_plan(self):
        """
        Gets the work_plan of this ValidateWorkPlanResponse.
        The work plan reference associated with this response

        :return: The work_plan of this ValidateWorkPlanResponse.
        :rtype: WorkPlanReference
        """
        return self._work_plan

    @work_plan.setter
    def work_plan(self, work_plan):
        """
        Sets the work_plan of this ValidateWorkPlanResponse.
        The work plan reference associated with this response

        :param work_plan: The work_plan of this ValidateWorkPlanResponse.
        :type: WorkPlanReference
        """
        
        self._work_plan = work_plan

    @property
    def valid(self):
        """
        Gets the valid of this ValidateWorkPlanResponse.
        Whether the work plan is valid or not

        :return: The valid of this ValidateWorkPlanResponse.
        :rtype: bool
        """
        return self._valid

    @valid.setter
    def valid(self, valid):
        """
        Sets the valid of this ValidateWorkPlanResponse.
        Whether the work plan is valid or not

        :param valid: The valid of this ValidateWorkPlanResponse.
        :type: bool
        """
        
        self._valid = valid

    @property
    def messages(self):
        """
        Gets the messages of this ValidateWorkPlanResponse.
        Validation messages for this work plan

        :return: The messages of this ValidateWorkPlanResponse.
        :rtype: ValidateWorkPlanMessages
        """
        return self._messages

    @messages.setter
    def messages(self, messages):
        """
        Sets the messages of this ValidateWorkPlanResponse.
        Validation messages for this work plan

        :param messages: The messages of this ValidateWorkPlanResponse.
        :type: ValidateWorkPlanMessages
        """
        
        self._messages = messages

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

