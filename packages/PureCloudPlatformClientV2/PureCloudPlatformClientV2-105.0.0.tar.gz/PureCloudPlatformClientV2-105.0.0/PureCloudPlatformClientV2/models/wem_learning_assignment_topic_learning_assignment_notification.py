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

class WemLearningAssignmentTopicLearningAssignmentNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WemLearningAssignmentTopicLearningAssignmentNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'user': 'WemLearningAssignmentTopicUserReference',
            'module': 'WemLearningAssignmentTopicLearningModuleReference',
            'version': 'int',
            'state': 'str',
            'date_recommended_for_completion': 'datetime',
            'created_by': 'WemLearningAssignmentTopicUserReference',
            'date_created': 'datetime',
            'modified_by': 'WemLearningAssignmentTopicUserReference',
            'date_modified': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'user': 'user',
            'module': 'module',
            'version': 'version',
            'state': 'state',
            'date_recommended_for_completion': 'dateRecommendedForCompletion',
            'created_by': 'createdBy',
            'date_created': 'dateCreated',
            'modified_by': 'modifiedBy',
            'date_modified': 'dateModified'
        }

        self._id = None
        self._user = None
        self._module = None
        self._version = None
        self._state = None
        self._date_recommended_for_completion = None
        self._created_by = None
        self._date_created = None
        self._modified_by = None
        self._date_modified = None

    @property
    def id(self):
        """
        Gets the id of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The id of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param id: The id of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: str
        """
        
        self._id = id

    @property
    def user(self):
        """
        Gets the user of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The user of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: WemLearningAssignmentTopicUserReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param user: The user of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: WemLearningAssignmentTopicUserReference
        """
        
        self._user = user

    @property
    def module(self):
        """
        Gets the module of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The module of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: WemLearningAssignmentTopicLearningModuleReference
        """
        return self._module

    @module.setter
    def module(self, module):
        """
        Sets the module of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param module: The module of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: WemLearningAssignmentTopicLearningModuleReference
        """
        
        self._module = module

    @property
    def version(self):
        """
        Gets the version of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The version of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param version: The version of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: int
        """
        
        self._version = version

    @property
    def state(self):
        """
        Gets the state of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The state of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param state: The state of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: str
        """
        allowed_values = ["Assigned", "InProgress", "Completed", "Deleted"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def date_recommended_for_completion(self):
        """
        Gets the date_recommended_for_completion of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The date_recommended_for_completion of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: datetime
        """
        return self._date_recommended_for_completion

    @date_recommended_for_completion.setter
    def date_recommended_for_completion(self, date_recommended_for_completion):
        """
        Sets the date_recommended_for_completion of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param date_recommended_for_completion: The date_recommended_for_completion of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: datetime
        """
        
        self._date_recommended_for_completion = date_recommended_for_completion

    @property
    def created_by(self):
        """
        Gets the created_by of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The created_by of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: WemLearningAssignmentTopicUserReference
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param created_by: The created_by of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: WemLearningAssignmentTopicUserReference
        """
        
        self._created_by = created_by

    @property
    def date_created(self):
        """
        Gets the date_created of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The date_created of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param date_created: The date_created of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def modified_by(self):
        """
        Gets the modified_by of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The modified_by of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: WemLearningAssignmentTopicUserReference
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param modified_by: The modified_by of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: WemLearningAssignmentTopicUserReference
        """
        
        self._modified_by = modified_by

    @property
    def date_modified(self):
        """
        Gets the date_modified of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :return: The date_modified of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this WemLearningAssignmentTopicLearningAssignmentNotification.


        :param date_modified: The date_modified of this WemLearningAssignmentTopicLearningAssignmentNotification.
        :type: datetime
        """
        
        self._date_modified = date_modified

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

