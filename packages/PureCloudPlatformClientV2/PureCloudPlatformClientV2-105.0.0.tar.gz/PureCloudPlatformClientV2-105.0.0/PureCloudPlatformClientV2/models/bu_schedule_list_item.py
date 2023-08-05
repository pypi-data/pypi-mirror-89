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

class BuScheduleListItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuScheduleListItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'week_date': 'date',
            'week_count': 'int',
            'description': 'str',
            'published': 'bool',
            'short_term_forecast': 'BuShortTermForecastReference',
            'generation_results': 'ScheduleGenerationResultSummary',
            'metadata': 'WfmVersionedEntityMetadata',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'week_date': 'weekDate',
            'week_count': 'weekCount',
            'description': 'description',
            'published': 'published',
            'short_term_forecast': 'shortTermForecast',
            'generation_results': 'generationResults',
            'metadata': 'metadata',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._week_date = None
        self._week_count = None
        self._description = None
        self._published = None
        self._short_term_forecast = None
        self._generation_results = None
        self._metadata = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this BuScheduleListItem.
        The globally unique identifier for the object.

        :return: The id of this BuScheduleListItem.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BuScheduleListItem.
        The globally unique identifier for the object.

        :param id: The id of this BuScheduleListItem.
        :type: str
        """
        
        self._id = id

    @property
    def week_date(self):
        """
        Gets the week_date of this BuScheduleListItem.
        The start week date for this schedule. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The week_date of this BuScheduleListItem.
        :rtype: date
        """
        return self._week_date

    @week_date.setter
    def week_date(self, week_date):
        """
        Sets the week_date of this BuScheduleListItem.
        The start week date for this schedule. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param week_date: The week_date of this BuScheduleListItem.
        :type: date
        """
        
        self._week_date = week_date

    @property
    def week_count(self):
        """
        Gets the week_count of this BuScheduleListItem.
        The number of weeks spanned by this schedule

        :return: The week_count of this BuScheduleListItem.
        :rtype: int
        """
        return self._week_count

    @week_count.setter
    def week_count(self, week_count):
        """
        Sets the week_count of this BuScheduleListItem.
        The number of weeks spanned by this schedule

        :param week_count: The week_count of this BuScheduleListItem.
        :type: int
        """
        
        self._week_count = week_count

    @property
    def description(self):
        """
        Gets the description of this BuScheduleListItem.
        The description of this schedule

        :return: The description of this BuScheduleListItem.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this BuScheduleListItem.
        The description of this schedule

        :param description: The description of this BuScheduleListItem.
        :type: str
        """
        
        self._description = description

    @property
    def published(self):
        """
        Gets the published of this BuScheduleListItem.
        Whether this schedule is published

        :return: The published of this BuScheduleListItem.
        :rtype: bool
        """
        return self._published

    @published.setter
    def published(self, published):
        """
        Sets the published of this BuScheduleListItem.
        Whether this schedule is published

        :param published: The published of this BuScheduleListItem.
        :type: bool
        """
        
        self._published = published

    @property
    def short_term_forecast(self):
        """
        Gets the short_term_forecast of this BuScheduleListItem.
        The forecast used for this schedule, if applicable

        :return: The short_term_forecast of this BuScheduleListItem.
        :rtype: BuShortTermForecastReference
        """
        return self._short_term_forecast

    @short_term_forecast.setter
    def short_term_forecast(self, short_term_forecast):
        """
        Sets the short_term_forecast of this BuScheduleListItem.
        The forecast used for this schedule, if applicable

        :param short_term_forecast: The short_term_forecast of this BuScheduleListItem.
        :type: BuShortTermForecastReference
        """
        
        self._short_term_forecast = short_term_forecast

    @property
    def generation_results(self):
        """
        Gets the generation_results of this BuScheduleListItem.
        Generation result summary for this schedule, if applicable

        :return: The generation_results of this BuScheduleListItem.
        :rtype: ScheduleGenerationResultSummary
        """
        return self._generation_results

    @generation_results.setter
    def generation_results(self, generation_results):
        """
        Sets the generation_results of this BuScheduleListItem.
        Generation result summary for this schedule, if applicable

        :param generation_results: The generation_results of this BuScheduleListItem.
        :type: ScheduleGenerationResultSummary
        """
        
        self._generation_results = generation_results

    @property
    def metadata(self):
        """
        Gets the metadata of this BuScheduleListItem.
        Version metadata for this schedule

        :return: The metadata of this BuScheduleListItem.
        :rtype: WfmVersionedEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this BuScheduleListItem.
        Version metadata for this schedule

        :param metadata: The metadata of this BuScheduleListItem.
        :type: WfmVersionedEntityMetadata
        """
        
        self._metadata = metadata

    @property
    def self_uri(self):
        """
        Gets the self_uri of this BuScheduleListItem.
        The URI for this object

        :return: The self_uri of this BuScheduleListItem.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this BuScheduleListItem.
        The URI for this object

        :param self_uri: The self_uri of this BuScheduleListItem.
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

