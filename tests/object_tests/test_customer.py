import pytest
from lxml import etree

from django_quickbooks.exceptions import ValidationError
from django_quickbooks.objects import Customer, BillAddress, ShipAddress


def test_create_customer_validation_with_error():
    with pytest.raises(ValidationError):
        Customer(
            ListID=12312,
            EditSequence='asdf',
            Name=1234,
            FullName=1234,
            IsActive='True',
            BillAddress='Somewhere near Amazon',
            CompanyName=1234,
            Phone=1234,
            AltPhone=1234,
            Fax=1234,
            Email=1234,
            Contact=1234,
            AltContact=1234
        )


def test_create_customer(sample_customer_data, sample_address_data):
    customer = Customer(
        **sample_customer_data,
        BillAddress=BillAddress(**sample_address_data),
        ShipAddress=ShipAddress(**sample_address_data),
    )

    assert customer.Name == sample_customer_data['Name']
    assert customer.IsActive == sample_customer_data['IsActive']
    assert customer.ListID == sample_customer_data['ListID']
    assert customer.EditSequence == sample_customer_data['EditSequence']
    assert customer.FullName == sample_customer_data['FullName']
    assert customer.CompanyName == sample_customer_data['CompanyName']
    assert customer.Phone == sample_customer_data['Phone']
    assert customer.AltPhone == sample_customer_data['AltPhone']
    assert customer.Fax == sample_customer_data['Fax']
    assert customer.Email == sample_customer_data['Email']
    assert customer.Contact == sample_customer_data['Contact']
    assert customer.AltContact == sample_customer_data['AltContact']

    assert isinstance(customer.BillAddress, BillAddress)
    assert isinstance(customer.ShipAddress, ShipAddress)


def test_create_customer_from_xml(sample_customer_xml, sample_customer_data, sample_address_data):
    root_lxml = etree.fromstring(sample_customer_xml)
    customer = Customer.from_lxml(root_lxml)
    assert customer.ListID == sample_customer_data['ListID']
    assert customer.TimeCreated == sample_customer_data['TimeCreated']
    assert customer.TimeModified == sample_customer_data['TimeModified']
    assert customer.EditSequence == sample_customer_data['EditSequence']
    assert customer.Name == sample_customer_data['Name']
    assert customer.FullName == sample_customer_data['FullName']
    assert customer.IsActive == sample_customer_data['IsActive']
    assert customer.CompanyName == sample_customer_data['CompanyName']
    assert customer.Phone == sample_customer_data['Phone']
    assert customer.AltPhone == sample_customer_data['AltPhone']
    assert customer.Fax == sample_customer_data['Fax']
    assert customer.Email == sample_customer_data['Email']
    assert customer.Contact == sample_customer_data['Contact']
    assert customer.AltContact == sample_customer_data['AltContact']

    assert customer.BillAddress == BillAddress(**sample_address_data)
    assert customer.ShipAddress == ShipAddress(**sample_address_data)
