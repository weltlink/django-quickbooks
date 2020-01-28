from copy import deepcopy

import pytest

from django_quickbooks.objects import Invoice, BillAddress, ShipAddress, Customer, InvoiceLine, ItemService
from django_quickbooks.services.invoice import InvoiceService


@pytest.fixture
def invoice_service():
    return InvoiceService()


@pytest.fixture
def sample_invoice_add(
        sample_invoice_data,
        sample_address_data,
        sample_customer_data,
        sample_invoice_item_service1_data,
        sample_invoice_item_service2_data,
        sample_invoice_line1_data,
        sample_invoice_line2_data
):
    invoice_data = deepcopy(sample_invoice_data)
    invoice_data.pop('TxnID')
    invoice_data.pop('EditSequence')
    invoice_data.pop('TimeCreated')
    invoice_data.pop('TimeModified')
    invoice_line1_data = deepcopy(sample_invoice_line1_data)
    invoice_line2_data = deepcopy(sample_invoice_line2_data)
    invoice_line1_data.pop('TxnLineID')
    invoice_line2_data.pop('TxnLineID')
    sample_invoice_item_service1_data.pop('FullName')
    sample_invoice_item_service2_data.pop('FullName')
    customer_data = dict(ListID=sample_customer_data['ListID'], FullName=sample_customer_data['FullName'])

    return Invoice(
        **invoice_data,
        BillAddress=BillAddress(**sample_address_data),
        ShipAddress=ShipAddress(**sample_address_data),
        Customer=Customer(**customer_data),
        InvoiceLine=[
            InvoiceLine(**invoice_line1_data, Item=ItemService(**sample_invoice_item_service1_data)),
            InvoiceLine(**invoice_line2_data, Item=ItemService(**sample_invoice_item_service2_data))
        ]
    )


@pytest.fixture
def sample_invoice_add_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <InvoiceAddRq>
            <InvoiceAdd>
                <TxnDate>2018-03-24T00:31:04+05:00</TxnDate>
                <CustomerRef>
                    <ListID>800004ED-1525972764</ListID>
                    <FullName>Amazon</FullName>
                </CustomerRef>
                <BillAddress>
                    <Addr1>2305 Litton Ln</Addr1>
                    <City>Hebron</City>
                    <State>Kentucky</State>
                    <PostalCode>41048</PostalCode>
                    <Country>United States</Country>
                    <Note>Nice address</Note>
                </BillAddress>
                <IsPending>true</IsPending>
                <DueDate>2018-03-24T00:31:04+05:00</DueDate>
                <Memo>a2e8929f-6f03-4bc2-ad27-ea6aa2cc11cd</Memo>
                <InvoiceLineAdd>
                    <ItemRef>
                        <ListID>800004ED-1525972764</ListID>
                    </ItemRef>
                    <Desc>First Line of Invoice</Desc>
                    <Quantity>1.0</Quantity>
                    <Rate>500.5</Rate>
                </InvoiceLineAdd>
                <InvoiceLineAdd>
                    <ItemRef>
                        <ListID>800004ED-1525972765</ListID>
                    </ItemRef>
                    <Desc>Second Line of Invoice</Desc>
                    <Quantity>1.0</Quantity>
                    <Rate>100.5</Rate>
                </InvoiceLineAdd>
            </InvoiceAdd>
        </InvoiceAddRq>
    </QBXMLMsgsRq>
</QBXML>
    """


def test_invoice_service_add(
        invoice_service,
        sample_invoice_add,
        sample_invoice_add_xml,
        xml_compare_fn
):
    checking_xml = invoice_service.add(sample_invoice_add)
    xml_compare_fn(checking_xml, sample_invoice_add_xml)


@pytest.fixture
def sample_invoice_mod(
        sample_invoice_add,
        sample_invoice_line1_data,
        sample_invoice_line2_data,
        sample_invoice_data
):
    invoice = sample_invoice_add
    invoice.TxnID = sample_invoice_data['TxnID']
    invoice.EditSequence = sample_invoice_data['EditSequence']
    invoice.InvoiceLine[0].TxnLineID = sample_invoice_line1_data['TxnLineID']
    invoice.InvoiceLine[1].TxnLineID = sample_invoice_line2_data['TxnLineID']

    return invoice


@pytest.fixture
def sample_invoice_mod_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <InvoiceModRq>
            <InvoiceMod>
                <TxnID>800004ED-1525972764</TxnID>
                <EditSequence>1525972764</EditSequence>
                <TxnDate>2018-03-24T00:31:04+05:00</TxnDate>
                <CustomerRef>
                    <ListID>800004ED-1525972764</ListID>
                    <FullName>Amazon</FullName>
                </CustomerRef>
                <BillAddress>
                    <Addr1>2305 Litton Ln</Addr1>
                    <City>Hebron</City>
                    <State>Kentucky</State>
                    <PostalCode>41048</PostalCode>
                    <Country>United States</Country>
                    <Note>Nice address</Note>
                </BillAddress>
                <IsPending>true</IsPending>
                <DueDate>2018-03-24T00:31:04+05:00</DueDate>
                <Memo>a2e8929f-6f03-4bc2-ad27-ea6aa2cc11cd</Memo>
                <InvoiceLineMod>
                    <TxnLineID>800004ED-1525972764</TxnLineID>
                    <ItemRef>
                        <ListID>800004ED-1525972764</ListID>
                    </ItemRef>
                    <Desc>First Line of Invoice</Desc>
                    <Quantity>1.0</Quantity>
                    <Rate>500.5</Rate>
                </InvoiceLineMod>
                <InvoiceLineMod>
                    <TxnLineID>800004ED-1525972765</TxnLineID>
                    <ItemRef>
                        <ListID>800004ED-1525972765</ListID>
                    </ItemRef>
                    <Desc>Second Line of Invoice</Desc>
                    <Quantity>1.0</Quantity>
                    <Rate>100.5</Rate>
                </InvoiceLineMod>
            </InvoiceMod>
        </InvoiceModRq>
    </QBXMLMsgsRq>
</QBXML>
    """


def test_invoice_service_update(
        invoice_service,
        sample_invoice_mod,
        sample_invoice_mod_xml,
        xml_compare_fn
):
    checking_xml = invoice_service.update(sample_invoice_mod)
    xml_compare_fn(checking_xml, sample_invoice_mod_xml)


@pytest.fixture
def sample_invoice_query_all_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
        <QBXML>
            <QBXMLMsgsRq onError="stopOnError">
                <InvoiceQueryRq metaData="NoMetaData" iterator="Start">
                    <MaxReturned>100</MaxReturned>
                </InvoiceQueryRq>
            </QBXMLMsgsRq>
        </QBXML>
    """


def test_invoice_service_query_all(
        invoice_service,
        sample_invoice_query_all_xml,
        xml_compare_fn
):
    checking_xml = invoice_service.all()
    xml_compare_fn(checking_xml, sample_invoice_query_all_xml)


@pytest.fixture
def sample_invoice_query_id_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <InvoiceQueryRq metaData="NoMetaData">
            <TxnID>800004ED-1525972764</TxnID>
        </InvoiceQueryRq>
    </QBXMLMsgsRq>
</QBXML>
    """


def test_invoice_service_query_id(invoice_service, sample_invoice_query_id_xml, xml_compare_fn):
    checking_xml = invoice_service.find_by_id('800004ED-1525972764')
    xml_compare_fn(checking_xml, sample_invoice_query_id_xml)


@pytest.fixture
def sample_invoice_void_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <TxnVoidRq>
            <TxnID>800004ED-1525972764</TxnID>
            <TxnVoidType>Invoice</TxnVoidType>
        </TxnVoidRq>
    </QBXMLMsgsRq>
</QBXML>
    """


def test_invoice_service_void(invoice_service, sample_invoice_mod, sample_invoice_void_xml, xml_compare_fn):
    checking_xml = invoice_service.void(sample_invoice_mod)
    xml_compare_fn(checking_xml, sample_invoice_void_xml)


@pytest.fixture
def sample_invoice_delete_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <TxnDelRq>
            <TxnID>800004ED-1525972764</TxnID>
            <TxnDelType>Invoice</TxnDelType>
        </TxnDelRq>
    </QBXMLMsgsRq>
</QBXML>
    """


def test_invoice_service_delete(invoice_service, sample_invoice_mod, sample_invoice_delete_xml, xml_compare_fn):
    checking_xml = invoice_service.delete(sample_invoice_mod)
    xml_compare_fn(checking_xml, sample_invoice_delete_xml)
