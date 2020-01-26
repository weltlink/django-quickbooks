import pytest
from lxml import etree

from django_quickbooks.exceptions import ValidationError
from django_quickbooks.objects import Customer, BillAddress, ShipAddress


def test_create_customer_validation_with_error():
    with pytest.raises(ValidationError):
        Customer(ListID=12312)

    with pytest.raises(ValidationError):
        Customer(EditSequence='asdf')

    with pytest.raises(ValidationError):
        Customer(Name=1234)

    with pytest.raises(ValidationError):
        Customer(FullName=1234)

    with pytest.raises(ValidationError):
        Customer(IsActive='True')

    with pytest.raises(ValidationError):
        Customer(BillAddress='Somewhere near Amazon')

    with pytest.raises(ValidationError):
        Customer(CompanyName=1234)

    with pytest.raises(ValidationError):
        Customer(Phone=1234)

    with pytest.raises(ValidationError):
        Customer(AltPhone=1234)

    with pytest.raises(ValidationError):
        Customer(Fax=1234)

    with pytest.raises(ValidationError):
        Customer(Email=1234)

    with pytest.raises(ValidationError):
        Customer(Contact=1234)

    with pytest.raises(ValidationError):
        Customer(AltContact=1234)


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
