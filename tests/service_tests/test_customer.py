from copy import deepcopy

import pytest

from django_quickbooks.objects import BillAddress, ShipAddress, Customer
from django_quickbooks.services.customer import CustomerService


@pytest.fixture
def customer_service():
    return CustomerService()


@pytest.fixture
def sample_customer_add(
        sample_customer_data,
        sample_address_data,
):
    customer_data = deepcopy(sample_customer_data)
    customer_data.pop('ListID')
    customer_data.pop('TimeCreated')
    customer_data.pop('TimeModified')
    customer_data.pop('EditSequence')

    return Customer(
        **customer_data,
        BillAddress=BillAddress(**sample_address_data),
        ShipAddress=ShipAddress(**sample_address_data),
    )


@pytest.fixture
def sample_customer_add_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <CustomerAddRq>
            <CustomerAdd>
                <Name>Amazon</Name>
                <FullName>Amazon</FullName>
                <IsActive>true</IsActive>
                <CompanyName>Amazon</CompanyName>
                <BillAddress>
                    <Addr1>2305 Litton Ln</Addr1>
                    <City>Hebron</City>
                    <State>Kentucky</State>
                    <PostalCode>41048</PostalCode>
                    <Country>United States</Country>
                    <Note>Nice address</Note>
                </BillAddress>
                <ShipAddress>
                    <Addr1>2305 Litton Ln</Addr1>
                    <City>Hebron</City>
                    <State>Kentucky</State>
                    <PostalCode>41048</PostalCode>
                    <Country>United States</Country>
                    <Note>Nice address</Note>
                </ShipAddress>
                <Phone>998909090909</Phone>
                <AltPhone>998909090910</AltPhone>
                <Fax>998909090911</Fax>
                <Email>info@amazon.com</Email>
                <Contact>Someone from Amazon</Contact>
                <AltContact>Some other one from Amazon</AltContact>
            </CustomerAdd>
        </CustomerAddRq>
    </QBXMLMsgsRq>
</QBXML>"""


def test_customer_service_add(
        customer_service,
        sample_customer_add,
        sample_customer_add_xml,
        xml_compare_fn
):
    checking_xml = customer_service.add(sample_customer_add)
    xml_compare_fn(checking_xml, sample_customer_add_xml)


@pytest.fixture
def sample_customer_mod(
        sample_customer_add,
        sample_customer_data
):
    customer = deepcopy(sample_customer_add)
    customer.ListID = sample_customer_data['ListID']
    customer.EditSequence = sample_customer_data['EditSequence']

    return customer


@pytest.fixture
def sample_customer_mod_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <CustomerModRq>
            <CustomerMod>
                <ListID>800004ED-1525972764</ListID>
                <EditSequence>1525972764</EditSequence>
                <Name>Amazon</Name>
                <FullName>Amazon</FullName>
                <IsActive>true</IsActive>
                <CompanyName>Amazon</CompanyName>
                <BillAddress>
                    <Addr1>2305 Litton Ln</Addr1>
                    <City>Hebron</City>
                    <State>Kentucky</State>
                    <PostalCode>41048</PostalCode>
                    <Country>United States</Country>
                    <Note>Nice address</Note>
                </BillAddress>
                <ShipAddress>
                    <Addr1>2305 Litton Ln</Addr1>
                    <City>Hebron</City>
                    <State>Kentucky</State>
                    <PostalCode>41048</PostalCode>
                    <Country>United States</Country>
                    <Note>Nice address</Note>
                </ShipAddress>
                <Phone>998909090909</Phone>
                <AltPhone>998909090910</AltPhone>
                <Fax>998909090911</Fax>
                <Email>info@amazon.com</Email>
                <Contact>Someone from Amazon</Contact>
                <AltContact>Some other one from Amazon</AltContact>
            </CustomerMod>
        </CustomerModRq>
    </QBXMLMsgsRq>
</QBXML>"""


def test_customer_service_update(
        customer_service,
        sample_customer_mod,
        sample_customer_mod_xml,
        xml_compare_fn
):
    checking_xml = customer_service.update(sample_customer_mod)
    xml_compare_fn(checking_xml, sample_customer_mod_xml)


@pytest.fixture
def sample_customer_query_all_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <CustomerQueryRq metaData="NoMetaData" iterator="Start">
            <MaxReturned>100</MaxReturned>
        </CustomerQueryRq>
    </QBXMLMsgsRq>
</QBXML>"""


def test_customer_service_query_all(
        customer_service,
        sample_customer_query_all_xml,
        xml_compare_fn
):
    checking_xml = customer_service.all()
    xml_compare_fn(checking_xml, sample_customer_query_all_xml)


@pytest.fixture
def sample_customer_query_id_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <CustomerQueryRq metaData="NoMetaData">
            <ListID>800004ED-1525972764</ListID>
        </CustomerQueryRq>
    </QBXMLMsgsRq>
</QBXML>"""


def test_customer_service_query_id(customer_service, sample_customer_query_id_xml, xml_compare_fn):
    checking_xml = customer_service.find_by_id('800004ED-1525972764')
    xml_compare_fn(checking_xml, sample_customer_query_id_xml)


@pytest.fixture
def sample_customer_query_full_name_xml():
    return """<?xml version="1.0"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <CustomerQueryRq metaData="NoMetaData">
            <FullName>Amazon</FullName>
        </CustomerQueryRq>
    </QBXMLMsgsRq>
</QBXML>"""


def test_customer_service_query_full_name(customer_service, sample_customer_query_full_name_xml, xml_compare_fn):
    checking_xml = customer_service.find_by_full_name('Amazon')
    xml_compare_fn(checking_xml, sample_customer_query_full_name_xml)
