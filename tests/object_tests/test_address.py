from lxml import etree
import pytest

from django_quickbooks.exceptions import ValidationError
from django_quickbooks.objects import BillAddress, ShipAddress


def test_create_bill_address_with_validation_error():
    with pytest.raises(ValidationError):
        BillAddress(
            Addr1=12312,
            City=1234,
            State=1234,
            PostalCode=1234,
            Country=1234,
        )


def test_create_bill_address(sample_address_data):
    address = BillAddress(**sample_address_data)

    assert address.Addr1 == sample_address_data['Addr1']
    assert address.City == sample_address_data['City']
    assert address.State == sample_address_data['State']
    assert address.PostalCode == sample_address_data['PostalCode']
    assert address.Country == sample_address_data['Country']
    assert address.Note == sample_address_data['Note']


def test_create_bill_address_from_xml(sample_address_xml, sample_address_data):
    root_lxml = etree.fromstring(sample_address_xml)
    bill_address = BillAddress.from_lxml(root_lxml)
    assert bill_address.Addr1 == sample_address_data['Addr1']
    assert bill_address.City == sample_address_data['City']
    assert bill_address.State == sample_address_data['State']
    assert bill_address.PostalCode == sample_address_data['PostalCode']
    assert bill_address.Country == sample_address_data['Country']
    assert bill_address.Note == sample_address_data['Note']
