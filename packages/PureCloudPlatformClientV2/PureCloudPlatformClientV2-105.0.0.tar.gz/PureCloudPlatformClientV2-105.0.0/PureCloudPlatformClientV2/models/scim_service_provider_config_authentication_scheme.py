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

class ScimServiceProviderConfigAuthenticationScheme(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ScimServiceProviderConfigAuthenticationScheme - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'spec_uri': 'str',
            'documentation_uri': 'str',
            'type': 'str',
            'primary': 'bool'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'spec_uri': 'specUri',
            'documentation_uri': 'documentationUri',
            'type': 'type',
            'primary': 'primary'
        }

        self._name = None
        self._description = None
        self._spec_uri = None
        self._documentation_uri = None
        self._type = None
        self._primary = None

    @property
    def name(self):
        """
        Gets the name of this ScimServiceProviderConfigAuthenticationScheme.
        The name of the authentication scheme, for example, HTTP Basic.

        :return: The name of this ScimServiceProviderConfigAuthenticationScheme.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ScimServiceProviderConfigAuthenticationScheme.
        The name of the authentication scheme, for example, HTTP Basic.

        :param name: The name of this ScimServiceProviderConfigAuthenticationScheme.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ScimServiceProviderConfigAuthenticationScheme.
        The description of the authentication scheme.

        :return: The description of this ScimServiceProviderConfigAuthenticationScheme.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ScimServiceProviderConfigAuthenticationScheme.
        The description of the authentication scheme.

        :param description: The description of this ScimServiceProviderConfigAuthenticationScheme.
        :type: str
        """
        
        self._description = description

    @property
    def spec_uri(self):
        """
        Gets the spec_uri of this ScimServiceProviderConfigAuthenticationScheme.
        The HTTP-addressable URL that points to the authentication scheme's specification.

        :return: The spec_uri of this ScimServiceProviderConfigAuthenticationScheme.
        :rtype: str
        """
        return self._spec_uri

    @spec_uri.setter
    def spec_uri(self, spec_uri):
        """
        Sets the spec_uri of this ScimServiceProviderConfigAuthenticationScheme.
        The HTTP-addressable URL that points to the authentication scheme's specification.

        :param spec_uri: The spec_uri of this ScimServiceProviderConfigAuthenticationScheme.
        :type: str
        """
        
        self._spec_uri = spec_uri

    @property
    def documentation_uri(self):
        """
        Gets the documentation_uri of this ScimServiceProviderConfigAuthenticationScheme.
        The HTTP-addressable URL that points to the authentication scheme's usage documentation.

        :return: The documentation_uri of this ScimServiceProviderConfigAuthenticationScheme.
        :rtype: str
        """
        return self._documentation_uri

    @documentation_uri.setter
    def documentation_uri(self, documentation_uri):
        """
        Sets the documentation_uri of this ScimServiceProviderConfigAuthenticationScheme.
        The HTTP-addressable URL that points to the authentication scheme's usage documentation.

        :param documentation_uri: The documentation_uri of this ScimServiceProviderConfigAuthenticationScheme.
        :type: str
        """
        
        self._documentation_uri = documentation_uri

    @property
    def type(self):
        """
        Gets the type of this ScimServiceProviderConfigAuthenticationScheme.
        The type of authentication scheme.

        :return: The type of this ScimServiceProviderConfigAuthenticationScheme.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ScimServiceProviderConfigAuthenticationScheme.
        The type of authentication scheme.

        :param type: The type of this ScimServiceProviderConfigAuthenticationScheme.
        :type: str
        """
        allowed_values = ["oauth", "oauth2", "oauthbearertoken", "httpbasic", "httpdigest"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def primary(self):
        """
        Gets the primary of this ScimServiceProviderConfigAuthenticationScheme.
        Indicates whether this authentication scheme is the primary method of authentication.

        :return: The primary of this ScimServiceProviderConfigAuthenticationScheme.
        :rtype: bool
        """
        return self._primary

    @primary.setter
    def primary(self, primary):
        """
        Sets the primary of this ScimServiceProviderConfigAuthenticationScheme.
        Indicates whether this authentication scheme is the primary method of authentication.

        :param primary: The primary of this ScimServiceProviderConfigAuthenticationScheme.
        :type: bool
        """
        
        self._primary = primary

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

