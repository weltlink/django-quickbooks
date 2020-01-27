import pytest
from lxml import etree

from django_quickbooks.exceptions import ValidationError
from django_quickbooks.objects import Customer, BillAddress, ShipAddress, Invoice, InvoiceLine, ItemService


def test_create_invoice_with_validation_error():
    with pytest.raises(ValidationError):
        Invoice(
            TxnID=12345,
            TimeCreated=12345,
            TimeModified=12345,
            EditSequence=12345,
            TxnDate=12345,
            IsPending=12345,
            DueDate=12345,
            Memo=12345,
            AltPhone=1234,
            Fax=1234,
            Email=1234,
            Contact=1234,
            AltContact=1234
        )


def test_create_invoice(
        sample_address_data,
        sample_customer_data,
        sample_invoice_item_service1_data,
        sample_invoice_item_service2_data,
        sample_invoice_line1_data,
        sample_invoice_line2_data,
        sample_invoice_data,
):
    invoice = Invoice(
        **sample_invoice_data,
        BillAddress=BillAddress(**sample_address_data),
        ShipAddress=ShipAddress(**sample_address_data),
        Customer=Customer(**sample_customer_data),
        InvoiceLine=[
            InvoiceLine(**sample_invoice_line1_data, Item=ItemService(**sample_invoice_item_service1_data)),
            InvoiceLine(**sample_invoice_item_service2_data, Item=ItemService(**sample_invoice_item_service2_data))
        ]
    )

    assert invoice.TxnID == sample_invoice_data['TxnID']
    assert invoice.TimeCreated == sample_invoice_data['TimeCreated']
    assert invoice.TimeModified == sample_invoice_data['TimeModified']
    assert invoice.EditSequence == sample_invoice_data['EditSequence']
    assert invoice.TxnDate == sample_invoice_data['TxnDate']
    assert invoice.IsPending == sample_invoice_data['IsPending']
    assert invoice.DueDate == sample_invoice_data['DueDate']
    assert invoice.Memo == sample_invoice_data['Memo']

    assert isinstance(invoice.BillAddress, BillAddress)
    assert isinstance(invoice.ShipAddress, ShipAddress)
    assert isinstance(invoice.Customer, Customer)
    assert isinstance(invoice.InvoiceLine, list)
    assert isinstance(invoice.InvoiceLine[0], InvoiceLine)
    assert isinstance(invoice.InvoiceLine[0].Item, ItemService)
    assert isinstance(invoice.InvoiceLine[1], InvoiceLine)


def test_create_invoice_from_xml(
        sample_invoice_xml,
        sample_address_data,
        sample_invoice_customer_data,
        sample_invoice_item_service1_data,
        sample_invoice_item_service2_data,
        sample_invoice_line1_data,
        sample_invoice_line2_data,
        sample_invoice_data,

):
    root_lxml = etree.fromstring(sample_invoice_xml)
    invoice = Invoice.from_lxml(root_lxml)

    assert invoice.TxnID == sample_invoice_data['TxnID']
    assert invoice.TimeCreated == sample_invoice_data['TimeCreated']
    assert invoice.TimeModified == sample_invoice_data['TimeModified']
    assert invoice.EditSequence == sample_invoice_data['EditSequence']
    assert invoice.IsPending == sample_invoice_data['IsPending']
    assert invoice.DueDate == sample_invoice_data['DueDate']
    assert invoice.Memo == sample_invoice_data['Memo']

    assert invoice.BillAddress == BillAddress(**sample_address_data)
    assert invoice.ShipAddress == ShipAddress(**sample_address_data)
    assert invoice.Customer == Customer(**sample_invoice_customer_data)

    assert isinstance(invoice.InvoiceLine, list)
    assert invoice.InvoiceLine[0] == InvoiceLine(
        **sample_invoice_line1_data,
        Item=ItemService(**sample_invoice_item_service1_data)
    )
    assert invoice.InvoiceLine[1] == InvoiceLine(
        **sample_invoice_line2_data,
        Item=ItemService(**sample_invoice_item_service2_data)
    )
