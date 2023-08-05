# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.2408
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class FxForwardAllOf(object):
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
        'start_date': 'datetime',
        'maturity_date': 'datetime',
        'dom_amount': 'float',
        'dom_ccy': 'str',
        'fgn_amount': 'float',
        'fgn_ccy': 'str',
        'ref_spot_rate': 'float',
        'is_ndf': 'bool',
        'fixing_date': 'datetime',
        'instrument_type': 'str'
    }

    attribute_map = {
        'start_date': 'startDate',
        'maturity_date': 'maturityDate',
        'dom_amount': 'domAmount',
        'dom_ccy': 'domCcy',
        'fgn_amount': 'fgnAmount',
        'fgn_ccy': 'fgnCcy',
        'ref_spot_rate': 'refSpotRate',
        'is_ndf': 'isNdf',
        'fixing_date': 'fixingDate',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'start_date': 'required',
        'maturity_date': 'required',
        'dom_amount': 'required',
        'dom_ccy': 'required',
        'fgn_amount': 'required',
        'fgn_ccy': 'required',
        'ref_spot_rate': 'optional',
        'is_ndf': 'optional',
        'fixing_date': 'optional',
        'instrument_type': 'required'
    }

    def __init__(self, start_date=None, maturity_date=None, dom_amount=None, dom_ccy=None, fgn_amount=None, fgn_ccy=None, ref_spot_rate=None, is_ndf=None, fixing_date=None, instrument_type=None):  # noqa: E501
        """
        FxForwardAllOf - a model defined in OpenAPI

        :param start_date:  The start date of the instrument. This is normally synonymous with the trade-date. (required)
        :type start_date: datetime
        :param maturity_date:  The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date (required)
        :type maturity_date: datetime
        :param dom_amount:  The amount that is to be paid in the domestic currency on the maturity date. (required)
        :type dom_amount: float
        :param dom_ccy:  The domestic currency of the instrument. (required)
        :type dom_ccy: str
        :param fgn_amount:  The amount that is to be paid in the foreign currency on the maturity date (required)
        :type fgn_amount: float
        :param fgn_ccy:  The foreign (other) currency of the instrument. In the NDF case, only payments are made in the domestic currency.              For the outright forward, currencies are exchanged. By domestic is then that of the portfolio. (required)
        :type fgn_ccy: str
        :param ref_spot_rate:  The reference Fx Spot rate for currency pair Foreign-Domestic that was seen on the trade start date (time).
        :type ref_spot_rate: float
        :param is_ndf:  Is the contract an Fx-Forward of \"Non-Deliverable\" type, meaning a single payment in the domestic currency based on the change in fx-rate vs              a reference rate is used.
        :type is_ndf: bool
        :param fixing_date:  The fixing date .
        :type fixing_date: datetime
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashflowLeg, Unknown, TermDeposit (required)
        :type instrument_type: str

        """  # noqa: E501

        self._start_date = None
        self._maturity_date = None
        self._dom_amount = None
        self._dom_ccy = None
        self._fgn_amount = None
        self._fgn_ccy = None
        self._ref_spot_rate = None
        self._is_ndf = None
        self._fixing_date = None
        self._instrument_type = None
        self.discriminator = None

        self.start_date = start_date
        self.maturity_date = maturity_date
        self.dom_amount = dom_amount
        self.dom_ccy = dom_ccy
        self.fgn_amount = fgn_amount
        self.fgn_ccy = fgn_ccy
        if ref_spot_rate is not None:
            self.ref_spot_rate = ref_spot_rate
        if is_ndf is not None:
            self.is_ndf = is_ndf
        if fixing_date is not None:
            self.fixing_date = fixing_date
        self.instrument_type = instrument_type

    @property
    def start_date(self):
        """Gets the start_date of this FxForwardAllOf.  # noqa: E501

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :return: The start_date of this FxForwardAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this FxForwardAllOf.

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :param start_date: The start_date of this FxForwardAllOf.  # noqa: E501
        :type: datetime
        """
        if start_date is None:
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def maturity_date(self):
        """Gets the maturity_date of this FxForwardAllOf.  # noqa: E501

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date  # noqa: E501

        :return: The maturity_date of this FxForwardAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._maturity_date

    @maturity_date.setter
    def maturity_date(self, maturity_date):
        """Sets the maturity_date of this FxForwardAllOf.

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date  # noqa: E501

        :param maturity_date: The maturity_date of this FxForwardAllOf.  # noqa: E501
        :type: datetime
        """
        if maturity_date is None:
            raise ValueError("Invalid value for `maturity_date`, must not be `None`")  # noqa: E501

        self._maturity_date = maturity_date

    @property
    def dom_amount(self):
        """Gets the dom_amount of this FxForwardAllOf.  # noqa: E501

        The amount that is to be paid in the domestic currency on the maturity date.  # noqa: E501

        :return: The dom_amount of this FxForwardAllOf.  # noqa: E501
        :rtype: float
        """
        return self._dom_amount

    @dom_amount.setter
    def dom_amount(self, dom_amount):
        """Sets the dom_amount of this FxForwardAllOf.

        The amount that is to be paid in the domestic currency on the maturity date.  # noqa: E501

        :param dom_amount: The dom_amount of this FxForwardAllOf.  # noqa: E501
        :type: float
        """
        if dom_amount is None:
            raise ValueError("Invalid value for `dom_amount`, must not be `None`")  # noqa: E501

        self._dom_amount = dom_amount

    @property
    def dom_ccy(self):
        """Gets the dom_ccy of this FxForwardAllOf.  # noqa: E501

        The domestic currency of the instrument.  # noqa: E501

        :return: The dom_ccy of this FxForwardAllOf.  # noqa: E501
        :rtype: str
        """
        return self._dom_ccy

    @dom_ccy.setter
    def dom_ccy(self, dom_ccy):
        """Sets the dom_ccy of this FxForwardAllOf.

        The domestic currency of the instrument.  # noqa: E501

        :param dom_ccy: The dom_ccy of this FxForwardAllOf.  # noqa: E501
        :type: str
        """
        if dom_ccy is None:
            raise ValueError("Invalid value for `dom_ccy`, must not be `None`")  # noqa: E501

        self._dom_ccy = dom_ccy

    @property
    def fgn_amount(self):
        """Gets the fgn_amount of this FxForwardAllOf.  # noqa: E501

        The amount that is to be paid in the foreign currency on the maturity date  # noqa: E501

        :return: The fgn_amount of this FxForwardAllOf.  # noqa: E501
        :rtype: float
        """
        return self._fgn_amount

    @fgn_amount.setter
    def fgn_amount(self, fgn_amount):
        """Sets the fgn_amount of this FxForwardAllOf.

        The amount that is to be paid in the foreign currency on the maturity date  # noqa: E501

        :param fgn_amount: The fgn_amount of this FxForwardAllOf.  # noqa: E501
        :type: float
        """
        if fgn_amount is None:
            raise ValueError("Invalid value for `fgn_amount`, must not be `None`")  # noqa: E501

        self._fgn_amount = fgn_amount

    @property
    def fgn_ccy(self):
        """Gets the fgn_ccy of this FxForwardAllOf.  # noqa: E501

        The foreign (other) currency of the instrument. In the NDF case, only payments are made in the domestic currency.              For the outright forward, currencies are exchanged. By domestic is then that of the portfolio.  # noqa: E501

        :return: The fgn_ccy of this FxForwardAllOf.  # noqa: E501
        :rtype: str
        """
        return self._fgn_ccy

    @fgn_ccy.setter
    def fgn_ccy(self, fgn_ccy):
        """Sets the fgn_ccy of this FxForwardAllOf.

        The foreign (other) currency of the instrument. In the NDF case, only payments are made in the domestic currency.              For the outright forward, currencies are exchanged. By domestic is then that of the portfolio.  # noqa: E501

        :param fgn_ccy: The fgn_ccy of this FxForwardAllOf.  # noqa: E501
        :type: str
        """
        if fgn_ccy is None:
            raise ValueError("Invalid value for `fgn_ccy`, must not be `None`")  # noqa: E501

        self._fgn_ccy = fgn_ccy

    @property
    def ref_spot_rate(self):
        """Gets the ref_spot_rate of this FxForwardAllOf.  # noqa: E501

        The reference Fx Spot rate for currency pair Foreign-Domestic that was seen on the trade start date (time).  # noqa: E501

        :return: The ref_spot_rate of this FxForwardAllOf.  # noqa: E501
        :rtype: float
        """
        return self._ref_spot_rate

    @ref_spot_rate.setter
    def ref_spot_rate(self, ref_spot_rate):
        """Sets the ref_spot_rate of this FxForwardAllOf.

        The reference Fx Spot rate for currency pair Foreign-Domestic that was seen on the trade start date (time).  # noqa: E501

        :param ref_spot_rate: The ref_spot_rate of this FxForwardAllOf.  # noqa: E501
        :type: float
        """

        self._ref_spot_rate = ref_spot_rate

    @property
    def is_ndf(self):
        """Gets the is_ndf of this FxForwardAllOf.  # noqa: E501

        Is the contract an Fx-Forward of \"Non-Deliverable\" type, meaning a single payment in the domestic currency based on the change in fx-rate vs              a reference rate is used.  # noqa: E501

        :return: The is_ndf of this FxForwardAllOf.  # noqa: E501
        :rtype: bool
        """
        return self._is_ndf

    @is_ndf.setter
    def is_ndf(self, is_ndf):
        """Sets the is_ndf of this FxForwardAllOf.

        Is the contract an Fx-Forward of \"Non-Deliverable\" type, meaning a single payment in the domestic currency based on the change in fx-rate vs              a reference rate is used.  # noqa: E501

        :param is_ndf: The is_ndf of this FxForwardAllOf.  # noqa: E501
        :type: bool
        """

        self._is_ndf = is_ndf

    @property
    def fixing_date(self):
        """Gets the fixing_date of this FxForwardAllOf.  # noqa: E501

        The fixing date .  # noqa: E501

        :return: The fixing_date of this FxForwardAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._fixing_date

    @fixing_date.setter
    def fixing_date(self, fixing_date):
        """Sets the fixing_date of this FxForwardAllOf.

        The fixing date .  # noqa: E501

        :param fixing_date: The fixing_date of this FxForwardAllOf.  # noqa: E501
        :type: datetime
        """

        self._fixing_date = fixing_date

    @property
    def instrument_type(self):
        """Gets the instrument_type of this FxForwardAllOf.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashflowLeg, Unknown, TermDeposit  # noqa: E501

        :return: The instrument_type of this FxForwardAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this FxForwardAllOf.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashflowLeg, Unknown, TermDeposit  # noqa: E501

        :param instrument_type: The instrument_type of this FxForwardAllOf.  # noqa: E501
        :type: str
        """
        if instrument_type is None:
            raise ValueError("Invalid value for `instrument_type`, must not be `None`")  # noqa: E501
        allowed_values = ["QuotedSecurity", "InterestRateSwap", "FxForward", "Future", "ExoticInstrument", "FxOption", "CreditDefaultSwap", "InterestRateSwaption", "Bond", "EquityOption", "FixedLeg", "FloatingLeg", "BespokeCashflowLeg", "Unknown", "TermDeposit"]  # noqa: E501
        if instrument_type not in allowed_values:
            raise ValueError(
                "Invalid value for `instrument_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_type, allowed_values)
            )

        self._instrument_type = instrument_type

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
        if not isinstance(other, FxForwardAllOf):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
