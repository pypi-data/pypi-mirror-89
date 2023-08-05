# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.2407
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class QuoteSeriesId(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'provider': 'str',
        'price_source': 'str',
        'instrument_id': 'str',
        'instrument_id_type': 'str',
        'quote_type': 'str',
        'field': 'str'
    }

    attribute_map = {
        'provider': 'provider',
        'price_source': 'priceSource',
        'instrument_id': 'instrumentId',
        'instrument_id_type': 'instrumentIdType',
        'quote_type': 'quoteType',
        'field': 'field'
    }

    required_map = {
        'provider': 'required',
        'price_source': 'optional',
        'instrument_id': 'required',
        'instrument_id_type': 'required',
        'quote_type': 'required',
        'field': 'required'
    }

    def __init__(self, provider=None, price_source=None, instrument_id=None, instrument_id_type=None, quote_type=None, field=None):  # noqa: E501
        """
        QuoteSeriesId - a model defined in OpenAPI

        :param provider:  The platform or vendor that provided the quote, e.g. 'DataScope', 'LUSID' etc. (required)
        :type provider: str
        :param price_source:  The source or originator of the quote, e.g. a bank or financial institution.
        :type price_source: str
        :param instrument_id:  The value of the instrument identifier that uniquely identifies the instrument that the quote is for, e.g. 'BBG00JX0P539'. (required)
        :type instrument_id: str
        :param instrument_id_type:  The type of instrument identifier used to uniquely identify the instrument that the quote is for, e.g. 'Figi'. The available values are: LusidInstrumentId, Figi, RIC, QuotePermId, Isin, CurrencyPair (required)
        :type instrument_id_type: str
        :param quote_type:  The type of the quote. This allows for quotes other than prices e.g. rates or spreads to be used. The available values are: Price, Spread, Rate, LogNormalVol, NormalVol, ParSpread, IsdaSpread, Upfront (required)
        :type quote_type: str
        :param field:  The field of the quote e.g. bid, mid, ask etc. This should be consistent across a time series of quotes. The allowed values are dependant on the specified Provider. (required)
        :type field: str

        """  # noqa: E501

        self._provider = None
        self._price_source = None
        self._instrument_id = None
        self._instrument_id_type = None
        self._quote_type = None
        self._field = None
        self.discriminator = None

        self.provider = provider
        self.price_source = price_source
        self.instrument_id = instrument_id
        self.instrument_id_type = instrument_id_type
        self.quote_type = quote_type
        self.field = field

    @property
    def provider(self):
        """Gets the provider of this QuoteSeriesId.  # noqa: E501

        The platform or vendor that provided the quote, e.g. 'DataScope', 'LUSID' etc.  # noqa: E501

        :return: The provider of this QuoteSeriesId.  # noqa: E501
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """Sets the provider of this QuoteSeriesId.

        The platform or vendor that provided the quote, e.g. 'DataScope', 'LUSID' etc.  # noqa: E501

        :param provider: The provider of this QuoteSeriesId.  # noqa: E501
        :type: str
        """
        if provider is None:
            raise ValueError("Invalid value for `provider`, must not be `None`")  # noqa: E501

        self._provider = provider

    @property
    def price_source(self):
        """Gets the price_source of this QuoteSeriesId.  # noqa: E501

        The source or originator of the quote, e.g. a bank or financial institution.  # noqa: E501

        :return: The price_source of this QuoteSeriesId.  # noqa: E501
        :rtype: str
        """
        return self._price_source

    @price_source.setter
    def price_source(self, price_source):
        """Sets the price_source of this QuoteSeriesId.

        The source or originator of the quote, e.g. a bank or financial institution.  # noqa: E501

        :param price_source: The price_source of this QuoteSeriesId.  # noqa: E501
        :type: str
        """

        self._price_source = price_source

    @property
    def instrument_id(self):
        """Gets the instrument_id of this QuoteSeriesId.  # noqa: E501

        The value of the instrument identifier that uniquely identifies the instrument that the quote is for, e.g. 'BBG00JX0P539'.  # noqa: E501

        :return: The instrument_id of this QuoteSeriesId.  # noqa: E501
        :rtype: str
        """
        return self._instrument_id

    @instrument_id.setter
    def instrument_id(self, instrument_id):
        """Sets the instrument_id of this QuoteSeriesId.

        The value of the instrument identifier that uniquely identifies the instrument that the quote is for, e.g. 'BBG00JX0P539'.  # noqa: E501

        :param instrument_id: The instrument_id of this QuoteSeriesId.  # noqa: E501
        :type: str
        """
        if instrument_id is None:
            raise ValueError("Invalid value for `instrument_id`, must not be `None`")  # noqa: E501

        self._instrument_id = instrument_id

    @property
    def instrument_id_type(self):
        """Gets the instrument_id_type of this QuoteSeriesId.  # noqa: E501

        The type of instrument identifier used to uniquely identify the instrument that the quote is for, e.g. 'Figi'. The available values are: LusidInstrumentId, Figi, RIC, QuotePermId, Isin, CurrencyPair  # noqa: E501

        :return: The instrument_id_type of this QuoteSeriesId.  # noqa: E501
        :rtype: str
        """
        return self._instrument_id_type

    @instrument_id_type.setter
    def instrument_id_type(self, instrument_id_type):
        """Sets the instrument_id_type of this QuoteSeriesId.

        The type of instrument identifier used to uniquely identify the instrument that the quote is for, e.g. 'Figi'. The available values are: LusidInstrumentId, Figi, RIC, QuotePermId, Isin, CurrencyPair  # noqa: E501

        :param instrument_id_type: The instrument_id_type of this QuoteSeriesId.  # noqa: E501
        :type: str
        """
        allowed_values = [None,"LusidInstrumentId", "Figi", "RIC", "QuotePermId", "Isin", "CurrencyPair"]  # noqa: E501
        if instrument_id_type not in allowed_values:
            raise ValueError(
                "Invalid value for `instrument_id_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_id_type, allowed_values)
            )

        self._instrument_id_type = instrument_id_type

    @property
    def quote_type(self):
        """Gets the quote_type of this QuoteSeriesId.  # noqa: E501

        The type of the quote. This allows for quotes other than prices e.g. rates or spreads to be used. The available values are: Price, Spread, Rate, LogNormalVol, NormalVol, ParSpread, IsdaSpread, Upfront  # noqa: E501

        :return: The quote_type of this QuoteSeriesId.  # noqa: E501
        :rtype: str
        """
        return self._quote_type

    @quote_type.setter
    def quote_type(self, quote_type):
        """Sets the quote_type of this QuoteSeriesId.

        The type of the quote. This allows for quotes other than prices e.g. rates or spreads to be used. The available values are: Price, Spread, Rate, LogNormalVol, NormalVol, ParSpread, IsdaSpread, Upfront  # noqa: E501

        :param quote_type: The quote_type of this QuoteSeriesId.  # noqa: E501
        :type: str
        """
        allowed_values = [None,"Price", "Spread", "Rate", "LogNormalVol", "NormalVol", "ParSpread", "IsdaSpread", "Upfront"]  # noqa: E501
        if quote_type not in allowed_values:
            raise ValueError(
                "Invalid value for `quote_type` ({0}), must be one of {1}"  # noqa: E501
                .format(quote_type, allowed_values)
            )

        self._quote_type = quote_type

    @property
    def field(self):
        """Gets the field of this QuoteSeriesId.  # noqa: E501

        The field of the quote e.g. bid, mid, ask etc. This should be consistent across a time series of quotes. The allowed values are dependant on the specified Provider.  # noqa: E501

        :return: The field of this QuoteSeriesId.  # noqa: E501
        :rtype: str
        """
        return self._field

    @field.setter
    def field(self, field):
        """Sets the field of this QuoteSeriesId.

        The field of the quote e.g. bid, mid, ask etc. This should be consistent across a time series of quotes. The allowed values are dependant on the specified Provider.  # noqa: E501

        :param field: The field of this QuoteSeriesId.  # noqa: E501
        :type: str
        """
        if field is None:
            raise ValueError("Invalid value for `field`, must not be `None`")  # noqa: E501

        self._field = field

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, QuoteSeriesId):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
