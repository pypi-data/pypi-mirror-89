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

class SegmentDetailQueryPredicate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SegmentDetailQueryPredicate - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'type': 'str',
            'dimension': 'str',
            'property_type': 'str',
            'pcProperty': 'str',
            'metric': 'str',
            'operator': 'str',
            'value': 'str',
            'range': 'NumericRange'
        }

        self.attribute_map = {
            'type': 'type',
            'dimension': 'dimension',
            'property_type': 'propertyType',
            'pcProperty': 'property',
            'metric': 'metric',
            'operator': 'operator',
            'value': 'value',
            'range': 'range'
        }

        self._type = None
        self._dimension = None
        self._property_type = None
        self._pcProperty = None
        self._metric = None
        self._operator = None
        self._value = None
        self._range = None

    @property
    def type(self):
        """
        Gets the type of this SegmentDetailQueryPredicate.
        Optional type, can usually be inferred

        :return: The type of this SegmentDetailQueryPredicate.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this SegmentDetailQueryPredicate.
        Optional type, can usually be inferred

        :param type: The type of this SegmentDetailQueryPredicate.
        :type: str
        """
        allowed_values = ["dimension", "property", "metric"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def dimension(self):
        """
        Gets the dimension of this SegmentDetailQueryPredicate.
        Left hand side for dimension predicates

        :return: The dimension of this SegmentDetailQueryPredicate.
        :rtype: str
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        """
        Sets the dimension of this SegmentDetailQueryPredicate.
        Left hand side for dimension predicates

        :param dimension: The dimension of this SegmentDetailQueryPredicate.
        :type: str
        """
        allowed_values = ["addressFrom", "addressOther", "addressSelf", "addressTo", "agentAssistantId", "agentRank", "agentScore", "ani", "audioMuted", "callbackNumber", "callbackScheduledTime", "callbackUserName", "cobrowseRole", "cobrowseRoomId", "conference", "destinationConversationId", "destinationSessionId", "direction", "disconnectType", "dispositionAnalyzer", "dispositionName", "dnis", "edgeId", "endingLanguage", "entryReason", "entryType", "errorCode", "exitReason", "externalContactId", "externalOrganizationId", "flaggedReason", "flowId", "flowName", "flowOutType", "flowOutcome", "flowOutcomeEndTimestamp", "flowOutcomeId", "flowOutcomeStartTimestamp", "flowOutcomeValue", "flowType", "flowVersion", "groupId", "issuedCallback", "journeyActionId", "journeyActionMapId", "journeyActionMapVersion", "journeyCustomerId", "journeyCustomerIdType", "journeyCustomerSessionId", "journeyCustomerSessionIdType", "journeySegmentScope", "mediaBridgeId", "mediaCount", "mediaType", "messageType", "monitoredParticipantId", "outboundCampaignId", "outboundContactId", "outboundContactListId", "participantId", "participantName", "peerId", "proposedAgentId", "protocolCallId", "provider", "purpose", "q850ResponseCode", "queueId", "recording", "remote", "remoteNameDisplayable", "requestedLanguageId", "requestedRouting", "requestedRoutingSkillId", "requestedRoutingUserId", "roomId", "scoredAgentId", "screenShareAddressSelf", "screenShareRoomId", "scriptId", "segmentEnd", "segmentType", "selectedAgentId", "selectedAgentRank", "sessionDnis", "sessionId", "sharingScreen", "sipResponseCode", "skipEnabled", "sourceConversationId", "sourceSessionId", "startingLanguage", "subject", "teamId", "timeoutSeconds", "transferTargetAddress", "transferTargetName", "transferType", "usedRouting", "userId", "videoAddressSelf", "videoMuted", "videoRoomId", "wrapUpCode", "wrapUpNote", "wrapUpTag"]
        if dimension.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for dimension -> " + dimension)
            self._dimension = "outdated_sdk_version"
        else:
            self._dimension = dimension

    @property
    def property_type(self):
        """
        Gets the property_type of this SegmentDetailQueryPredicate.
        Left hand side for property predicates

        :return: The property_type of this SegmentDetailQueryPredicate.
        :rtype: str
        """
        return self._property_type

    @property_type.setter
    def property_type(self, property_type):
        """
        Sets the property_type of this SegmentDetailQueryPredicate.
        Left hand side for property predicates

        :param property_type: The property_type of this SegmentDetailQueryPredicate.
        :type: str
        """
        allowed_values = ["bool", "integer", "real", "date", "string", "uuid"]
        if property_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for property_type -> " + property_type)
            self._property_type = "outdated_sdk_version"
        else:
            self._property_type = property_type

    @property
    def pcProperty(self):
        """
        Gets the pcProperty of this SegmentDetailQueryPredicate.
        Left hand side for property predicates

        :return: The pcProperty of this SegmentDetailQueryPredicate.
        :rtype: str
        """
        return self._pcProperty

    @pcProperty.setter
    def pcProperty(self, pcProperty):
        """
        Sets the pcProperty of this SegmentDetailQueryPredicate.
        Left hand side for property predicates

        :param pcProperty: The pcProperty of this SegmentDetailQueryPredicate.
        :type: str
        """
        
        self._pcProperty = pcProperty

    @property
    def metric(self):
        """
        Gets the metric of this SegmentDetailQueryPredicate.
        Left hand side for metric predicates

        :return: The metric of this SegmentDetailQueryPredicate.
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this SegmentDetailQueryPredicate.
        Left hand side for metric predicates

        :param metric: The metric of this SegmentDetailQueryPredicate.
        :type: str
        """
        allowed_values = ["tSegmentDuration"]
        if metric.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for metric -> " + metric)
            self._metric = "outdated_sdk_version"
        else:
            self._metric = metric

    @property
    def operator(self):
        """
        Gets the operator of this SegmentDetailQueryPredicate.
        Optional operator, default is matches

        :return: The operator of this SegmentDetailQueryPredicate.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """
        Sets the operator of this SegmentDetailQueryPredicate.
        Optional operator, default is matches

        :param operator: The operator of this SegmentDetailQueryPredicate.
        :type: str
        """
        allowed_values = ["matches", "exists", "notExists"]
        if operator.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for operator -> " + operator)
            self._operator = "outdated_sdk_version"
        else:
            self._operator = operator

    @property
    def value(self):
        """
        Gets the value of this SegmentDetailQueryPredicate.
        Right hand side for dimension, metric, or property predicates

        :return: The value of this SegmentDetailQueryPredicate.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this SegmentDetailQueryPredicate.
        Right hand side for dimension, metric, or property predicates

        :param value: The value of this SegmentDetailQueryPredicate.
        :type: str
        """
        
        self._value = value

    @property
    def range(self):
        """
        Gets the range of this SegmentDetailQueryPredicate.
        Right hand side for dimension, metric, or property predicates

        :return: The range of this SegmentDetailQueryPredicate.
        :rtype: NumericRange
        """
        return self._range

    @range.setter
    def range(self, range):
        """
        Sets the range of this SegmentDetailQueryPredicate.
        Right hand side for dimension, metric, or property predicates

        :param range: The range of this SegmentDetailQueryPredicate.
        :type: NumericRange
        """
        
        self._range = range

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

