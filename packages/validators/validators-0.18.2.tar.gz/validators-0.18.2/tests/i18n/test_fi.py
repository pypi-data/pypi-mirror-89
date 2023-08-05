# -*- coding: utf-8 -*-
import pytest

from validators import ValidationFailure
from validators.i18n.fi import fi_business_id, fi_ssn


@pytest.mark.parametrize(('value',), [
    ('2336509-6',),  # Supercell
    ('0112038-9',),  # Fast Monkeys
    ('2417581-7',),  # Nokia
])
def test_returns_true_on_valid_business_id(value):
    assert fi_business_id(value)


@pytest.mark.parametrize(('value',), [
    (None,),
    ('',),
    ('1233312312',),
    ('1333333-8',),
    ('1231233-9',),
])
def test_returns_failed_validation_on_invalid_business_id(value):
    assert isinstance(fi_business_id(value), ValidationFailure)


@pytest.mark.parametrize(('value',), [
    ('010190-002R',),
    ('010101-0101',),
    ('010101+0101',),
    ('010101A0101',),
    ('010190-900P',),
])
def test_returns_true_on_valid_ssn(value):
    assert fi_ssn(value)


@pytest.mark.parametrize(('value',), [
    (None,),
    ('',),
    ('010190-001P',),  # Too low serial
    ('010190-000N',),  # Too low serial
    ('000190-0023',),  # Invalid day
    ('010090-002X',),  # Invalid month
    ('010190-002r',),  # Invalid checksum
    ('101010-0102',),
    ('10a010-0101',),
    ('101010-0\xe401',),
    ('101010b0101',)
])
def test_returns_failed_validation_on_invalid_ssn(value):
    assert isinstance(fi_ssn(value), ValidationFailure)


def test_returns_failed_validation_on_temporal_ssn_when_not_allowed():
    assert isinstance(
        fi_ssn('010190-900P', allow_temporal_ssn=False),
        ValidationFailure
    )
