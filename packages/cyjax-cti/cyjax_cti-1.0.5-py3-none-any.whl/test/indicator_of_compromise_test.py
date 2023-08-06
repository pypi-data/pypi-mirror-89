#  CYjAX Limited

import datetime
import logging
from datetime import timedelta
from unittest.mock import patch, Mock

import pytest
import pytz

import cyjax
from cyjax import IndicatorOfCompromise, InvalidDateFormatException


class TestIndicatorOfCompromise:

    fake_date = Mock(wraps=datetime.datetime)
    fake_date.now.return_value.astimezone.return_value = datetime.datetime(2020, 5, 2, 12, 0, 0, tzinfo=pytz.UTC)

    def test_class_constants(self):
        assert 'IPv4' in IndicatorOfCompromise.SUPPORTED_TYPES
        assert 'IPv6' in IndicatorOfCompromise.SUPPORTED_TYPES
        assert 'Domain' in IndicatorOfCompromise.SUPPORTED_TYPES
        assert 'Email' in IndicatorOfCompromise.SUPPORTED_TYPES
        assert 'FileHash-SHA1' in IndicatorOfCompromise.SUPPORTED_TYPES
        assert 'FileHash-SHA256' in IndicatorOfCompromise.SUPPORTED_TYPES
        assert 'FileHash-MD5' in IndicatorOfCompromise.SUPPORTED_TYPES
        assert 'FileHash-SSDEEP' in IndicatorOfCompromise.SUPPORTED_TYPES

        assert 'incident-report' in IndicatorOfCompromise.SUPPORTED_SOURCES
        assert 'my-report' in IndicatorOfCompromise.SUPPORTED_SOURCES

    def test_get_indicator_of_compromise_without_parameters(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list()
        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params={})

    def test_get_indicator_of_compromise_with_parameters(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since='2020-05-02T07:31:11+00:00', until='2020-07-02T00:00:00+00:00')

        expected_params = {'since': '2020-05-02T07:31:11+00:00', 'until': '2020-07-02T00:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    @patch('cyjax.helpers.datetime', fake_date)
    def test_get_indicator_of_compromise_with_date_as_timedelta(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since=timedelta(hours=2), until=timedelta(hours=1))

        since = '2020-05-02T10:00:00+00:00'
        until = '2020-05-02T11:00:00+00:00'
        expected_params = {'since': since, 'until': until}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_date_as_datetime_without_timezone(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0),
                                     until=datetime.datetime(2020, 5, 2, 11, 0, 0))

        since = datetime.datetime(2020, 5, 2, 10, 0, 0).astimezone().isoformat()
        until = datetime.datetime(2020, 5, 2, 11, 0, 0).astimezone().isoformat()
        expected_params = {'since': since, 'until': until}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_date_as_datetime_with_timezone(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since=datetime.datetime(2020, 5, 2, 10, 0, 0, tzinfo=pytz.UTC),
                                     until=datetime.datetime(2020, 5, 2, 11, 0, 0, tzinfo=pytz.UTC))

        expected_params = {'since': '2020-05-02T10:00:00+00:00', 'until': '2020-05-02T11:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_date_as_string(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(since='2020-05-02T10:00:00+00:00', until='2020-05-02T11:00:00+00:00')

        expected_params = {'since': '2020-05-02T10:00:00+00:00', 'until': '2020-05-02T11:00:00+00:00'}

        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicator_of_compromise_with_wrong_date(self):
        indicator_of_compromise = IndicatorOfCompromise()
        with pytest.raises(InvalidDateFormatException):
            indicator_of_compromise.list(since='2020-05', until='2020-05-02T11:00:00+00:00')

        with pytest.raises(InvalidDateFormatException):
            indicator_of_compromise.list(since='2020-05-02T11:00:00+00:00', until='2020-05')

    def test_setting_client(self):
        cyjax.api_key = None  # reset to defaults

        resource = IndicatorOfCompromise()
        assert 'https://api.cyberportal.co' == resource._api_client.get_api_url()
        assert resource._api_client.get_api_key() is None

        resource = IndicatorOfCompromise('123456', 'https://api.new-address.com')
        assert 'https://api.new-address.com' == resource._api_client.get_api_url()
        assert '123456' == resource._api_client.get_api_key()

        cyjax.api_url = None  # Reset to default

    def test_get_one_is_not_implemented(self):
        resource = IndicatorOfCompromise()

        with pytest.raises(NotImplementedError) as e:
            resource.one(4)

    def test_get_indicators_with_type_filter(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(type='IPv6')
        expected_params = {'type': 'IPv6'}
        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicators_with_invalid_type_filter(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        with pytest.raises(ValueError) as e:
            indicator_of_compromise.list(type='not-supported')

        spy_method_paginate.assert_not_called()

    def test_get_indicators_with_source_type_filter(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(source_type='incident-report')
        expected_params = {'sourceType': 'incident-report'}
        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicators_with_invalid_source_type_filter(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        with pytest.raises(ValueError) as e:
            indicator_of_compromise.list(source_type='incidents')

        spy_method_paginate.assert_not_called()

    def test_get_indicators_with_source_id_filter(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        indicator_of_compromise.list(source_id=123)
        expected_params = {'sourceId': 123}
        spy_method_paginate.assert_called_once_with(endpoint='indicator-of-compromise', params=expected_params)

    def test_get_indicators_with_invalid_source_id_filter(self, mocker):
        indicator_of_compromise = IndicatorOfCompromise()
        spy_method_paginate = mocker.spy(indicator_of_compromise, 'paginate')

        with pytest.raises(ValueError) as e:
            indicator_of_compromise.list(source_id=0)

        spy_method_paginate.assert_not_called()
