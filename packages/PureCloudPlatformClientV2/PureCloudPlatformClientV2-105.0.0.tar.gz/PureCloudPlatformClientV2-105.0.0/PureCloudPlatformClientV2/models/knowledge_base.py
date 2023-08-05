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

class KnowledgeBase(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        KnowledgeBase - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'core_language': 'str',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'faq_count': 'int',
            'date_document_last_modified': 'datetime',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'core_language': 'coreLanguage',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'faq_count': 'faqCount',
            'date_document_last_modified': 'dateDocumentLastModified',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._core_language = None
        self._date_created = None
        self._date_modified = None
        self._faq_count = None
        self._date_document_last_modified = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this KnowledgeBase.
        The globally unique identifier for the object.

        :return: The id of this KnowledgeBase.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this KnowledgeBase.
        The globally unique identifier for the object.

        :param id: The id of this KnowledgeBase.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this KnowledgeBase.


        :return: The name of this KnowledgeBase.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this KnowledgeBase.


        :param name: The name of this KnowledgeBase.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this KnowledgeBase.
        Knowledge base description

        :return: The description of this KnowledgeBase.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this KnowledgeBase.
        Knowledge base description

        :param description: The description of this KnowledgeBase.
        :type: str
        """
        
        self._description = description

    @property
    def core_language(self):
        """
        Gets the core_language of this KnowledgeBase.
        Core language for knowledge base in which initial content must be created first

        :return: The core_language of this KnowledgeBase.
        :rtype: str
        """
        return self._core_language

    @core_language.setter
    def core_language(self, core_language):
        """
        Sets the core_language of this KnowledgeBase.
        Core language for knowledge base in which initial content must be created first

        :param core_language: The core_language of this KnowledgeBase.
        :type: str
        """
        allowed_values = ["en-US", "de-DE"]
        if core_language.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for core_language -> " + core_language)
            self._core_language = "outdated_sdk_version"
        else:
            self._core_language = core_language

    @property
    def date_created(self):
        """
        Gets the date_created of this KnowledgeBase.
        Knowledge base creation date-time. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this KnowledgeBase.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this KnowledgeBase.
        Knowledge base creation date-time. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this KnowledgeBase.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this KnowledgeBase.
        Knowledge base last modification date-time. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_modified of this KnowledgeBase.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this KnowledgeBase.
        Knowledge base last modification date-time. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_modified: The date_modified of this KnowledgeBase.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def faq_count(self):
        """
        Gets the faq_count of this KnowledgeBase.
        The count representing the number of documents of type FAQ per KnowledgeBase

        :return: The faq_count of this KnowledgeBase.
        :rtype: int
        """
        return self._faq_count

    @faq_count.setter
    def faq_count(self, faq_count):
        """
        Sets the faq_count of this KnowledgeBase.
        The count representing the number of documents of type FAQ per KnowledgeBase

        :param faq_count: The faq_count of this KnowledgeBase.
        :type: int
        """
        
        self._faq_count = faq_count

    @property
    def date_document_last_modified(self):
        """
        Gets the date_document_last_modified of this KnowledgeBase.
        The date representing when the last document is modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_document_last_modified of this KnowledgeBase.
        :rtype: datetime
        """
        return self._date_document_last_modified

    @date_document_last_modified.setter
    def date_document_last_modified(self, date_document_last_modified):
        """
        Sets the date_document_last_modified of this KnowledgeBase.
        The date representing when the last document is modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_document_last_modified: The date_document_last_modified of this KnowledgeBase.
        :type: datetime
        """
        
        self._date_document_last_modified = date_document_last_modified

    @property
    def self_uri(self):
        """
        Gets the self_uri of this KnowledgeBase.
        The URI for this object

        :return: The self_uri of this KnowledgeBase.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this KnowledgeBase.
        The URI for this object

        :param self_uri: The self_uri of this KnowledgeBase.
        :type: str
        """
        
        self._self_uri = self_uri

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

