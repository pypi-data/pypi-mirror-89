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

class VmPairingInfo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        VmPairingInfo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'meta_data': 'MetaData',
            'edge_id': 'str',
            'auth_token': 'str',
            'org_id': 'str'
        }

        self.attribute_map = {
            'meta_data': 'meta-data',
            'edge_id': 'edge-id',
            'auth_token': 'auth-token',
            'org_id': 'org-id'
        }

        self._meta_data = None
        self._edge_id = None
        self._auth_token = None
        self._org_id = None

    @property
    def meta_data(self):
        """
        Gets the meta_data of this VmPairingInfo.
        This is to be used to complete the setup process of a locally deployed virtual edge device.

        :return: The meta_data of this VmPairingInfo.
        :rtype: MetaData
        """
        return self._meta_data

    @meta_data.setter
    def meta_data(self, meta_data):
        """
        Sets the meta_data of this VmPairingInfo.
        This is to be used to complete the setup process of a locally deployed virtual edge device.

        :param meta_data: The meta_data of this VmPairingInfo.
        :type: MetaData
        """
        
        self._meta_data = meta_data

    @property
    def edge_id(self):
        """
        Gets the edge_id of this VmPairingInfo.


        :return: The edge_id of this VmPairingInfo.
        :rtype: str
        """
        return self._edge_id

    @edge_id.setter
    def edge_id(self, edge_id):
        """
        Sets the edge_id of this VmPairingInfo.


        :param edge_id: The edge_id of this VmPairingInfo.
        :type: str
        """
        
        self._edge_id = edge_id

    @property
    def auth_token(self):
        """
        Gets the auth_token of this VmPairingInfo.


        :return: The auth_token of this VmPairingInfo.
        :rtype: str
        """
        return self._auth_token

    @auth_token.setter
    def auth_token(self, auth_token):
        """
        Sets the auth_token of this VmPairingInfo.


        :param auth_token: The auth_token of this VmPairingInfo.
        :type: str
        """
        
        self._auth_token = auth_token

    @property
    def org_id(self):
        """
        Gets the org_id of this VmPairingInfo.


        :return: The org_id of this VmPairingInfo.
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """
        Sets the org_id of this VmPairingInfo.


        :param org_id: The org_id of this VmPairingInfo.
        :type: str
        """
        
        self._org_id = org_id

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

