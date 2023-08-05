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

class ContactListDivisionView(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ContactListDivisionView - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'division': 'Division',
            'column_names': 'list[str]',
            'phone_columns': 'list[ContactPhoneNumberColumn]',
            'import_status': 'ImportStatus',
            'size': 'int',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'division': 'division',
            'column_names': 'columnNames',
            'phone_columns': 'phoneColumns',
            'import_status': 'importStatus',
            'size': 'size',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._division = None
        self._column_names = None
        self._phone_columns = None
        self._import_status = None
        self._size = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ContactListDivisionView.
        The globally unique identifier for the object.

        :return: The id of this ContactListDivisionView.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ContactListDivisionView.
        The globally unique identifier for the object.

        :param id: The id of this ContactListDivisionView.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ContactListDivisionView.


        :return: The name of this ContactListDivisionView.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ContactListDivisionView.


        :param name: The name of this ContactListDivisionView.
        :type: str
        """
        
        self._name = name

    @property
    def division(self):
        """
        Gets the division of this ContactListDivisionView.
        The division to which this entity belongs.

        :return: The division of this ContactListDivisionView.
        :rtype: Division
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this ContactListDivisionView.
        The division to which this entity belongs.

        :param division: The division of this ContactListDivisionView.
        :type: Division
        """
        
        self._division = division

    @property
    def column_names(self):
        """
        Gets the column_names of this ContactListDivisionView.
        The names of the contact data columns.

        :return: The column_names of this ContactListDivisionView.
        :rtype: list[str]
        """
        return self._column_names

    @column_names.setter
    def column_names(self, column_names):
        """
        Sets the column_names of this ContactListDivisionView.
        The names of the contact data columns.

        :param column_names: The column_names of this ContactListDivisionView.
        :type: list[str]
        """
        
        self._column_names = column_names

    @property
    def phone_columns(self):
        """
        Gets the phone_columns of this ContactListDivisionView.
        Indicates which columns are phone numbers.

        :return: The phone_columns of this ContactListDivisionView.
        :rtype: list[ContactPhoneNumberColumn]
        """
        return self._phone_columns

    @phone_columns.setter
    def phone_columns(self, phone_columns):
        """
        Sets the phone_columns of this ContactListDivisionView.
        Indicates which columns are phone numbers.

        :param phone_columns: The phone_columns of this ContactListDivisionView.
        :type: list[ContactPhoneNumberColumn]
        """
        
        self._phone_columns = phone_columns

    @property
    def import_status(self):
        """
        Gets the import_status of this ContactListDivisionView.
        The status of the import process.

        :return: The import_status of this ContactListDivisionView.
        :rtype: ImportStatus
        """
        return self._import_status

    @import_status.setter
    def import_status(self, import_status):
        """
        Sets the import_status of this ContactListDivisionView.
        The status of the import process.

        :param import_status: The import_status of this ContactListDivisionView.
        :type: ImportStatus
        """
        
        self._import_status = import_status

    @property
    def size(self):
        """
        Gets the size of this ContactListDivisionView.
        The number of contacts in the ContactList.

        :return: The size of this ContactListDivisionView.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this ContactListDivisionView.
        The number of contacts in the ContactList.

        :param size: The size of this ContactListDivisionView.
        :type: int
        """
        
        self._size = size

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ContactListDivisionView.
        The URI for this object

        :return: The self_uri of this ContactListDivisionView.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ContactListDivisionView.
        The URI for this object

        :param self_uri: The self_uri of this ContactListDivisionView.
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

