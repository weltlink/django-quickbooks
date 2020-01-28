import pytest
from lxml import etree


@pytest.fixture
def sample_customer_xml():
    return """
    <CustomerRet> <!-- optional -->
        <ListID>800004ED-1525972764</ListID> <!-- required -->
        <TimeCreated>2018-03-24T00:31:04+05:00</TimeCreated> <!-- required -->
        <TimeModified>2018-03-24T00:31:04+05:00</TimeModified> <!-- required -->
        <EditSequence>1525972764</EditSequence> <!-- required -->
        <Name>Amazon</Name> <!-- required -->
        <FullName>Amazon</FullName> <!-- required -->
        <IsActive>true</IsActive> <!-- optional -->
        <CompanyName>Amazon</CompanyName> <!-- optional -->
        <BillAddress> <!-- optional -->
            <Addr1>2305 Litton Ln</Addr1> <!-- optional -->
            <Addr2></Addr2> <!-- optional -->
            <Addr3></Addr3> <!-- optional -->
            <Addr4></Addr4> <!-- optional -->
            <Addr5></Addr5> <!-- optional -->
            <City>Hebron</City> <!-- optional -->
            <State>Kentucky</State> <!-- optional -->
            <PostalCode>41048</PostalCode> <!-- optional -->
            <Country>United States</Country> <!-- optional -->
            <Note>Nice address</Note> <!-- optional -->
        </BillAddress>
        <ShipAddress> <!-- optional -->
            <Addr1>2305 Litton Ln</Addr1> <!-- optional -->
            <Addr2></Addr2> <!-- optional -->
            <Addr3></Addr3> <!-- optional -->
            <Addr4></Addr4> <!-- optional -->
            <Addr5></Addr5> <!-- optional -->
            <City>Hebron</City> <!-- optional -->
            <State>Kentucky</State> <!-- optional -->
            <PostalCode>41048</PostalCode> <!-- optional -->
            <Country>United States</Country> <!-- optional -->
            <Note>Nice address</Note> <!-- optional -->
        </ShipAddress>
        <Phone>998909090909</Phone> <!-- optional -->
        <AltPhone>998909090910</AltPhone> <!-- optional -->
        <Fax>998909090911</Fax> <!-- optional -->
        <Email>info@amazon.com</Email> <!-- optional -->
        <Contact>Someone from Amazon</Contact> <!-- optional -->
        <AltContact>Some other one from Amazon</AltContact> <!-- optional -->
    </CustomerRet>
    """


@pytest.fixture
def sample_customer_data():
    return dict(
        ListID='800004ED-1525972764',
        TimeCreated='2018-03-24T00:31:04+05:00',
        TimeModified='2018-03-24T00:31:04+05:00',
        EditSequence='1525972764',
        Name='Amazon',
        FullName='Amazon',
        IsActive=True,
        CompanyName='Amazon',
        Phone='998909090909',
        AltPhone='998909090910',
        Fax='998909090911',
        Email='info@amazon.com',
        Contact='Someone from Amazon',
        AltContact='Some other one from Amazon',
    )


@pytest.fixture
def sample_address_xml():
    return """
    <Address> <!-- optional -->
        <Addr1>2305 Litton Ln</Addr1> <!-- optional -->
        <Addr2></Addr2> <!-- optional -->
        <Addr3></Addr3> <!-- optional -->
        <Addr4></Addr4> <!-- optional -->
        <Addr5></Addr5> <!-- optional -->
        <City>Hebron</City> <!-- optional -->
        <State>Kentucky</State> <!-- optional -->
        <PostalCode>41048</PostalCode> <!-- optional -->
        <Country>United States</Country> <!-- optional -->
        <Note>Nice address</Note> <!-- optional -->
    </Address>
    """


@pytest.fixture
def sample_address_data():
    return dict(
        Addr1='2305 Litton Ln',
        City='Hebron',
        State='Kentucky',
        PostalCode='41048',
        Country='United States',
        Note='Nice address'
    )

@pytest.fixture
def sample_invoice_xml():
    return """
    <InvoiceRet> <!-- optional -->
        <TxnID>800004ED-1525972764</TxnID> <!-- required -->
        <TimeCreated>2018-03-24T00:31:04+05:00</TimeCreated> <!-- required -->
        <TimeModified>2018-03-24T00:31:04+05:00</TimeModified> <!-- required -->
        <EditSequence>1525972764</EditSequence> <!-- required -->
        <CustomerRef> <!-- required -->
            <ListID>800004ED-1525972764</ListID> <!-- optional -->
            <FullName>Amazon</FullName> <!-- optional -->
        </CustomerRef>
        <TxnDate>2018-03-24T00:31:04+05:00</TxnDate> <!-- required -->
        <BillAddress> <!-- optional -->
            <Addr1>2305 Litton Ln</Addr1> <!-- optional -->
            <Addr2></Addr2> <!-- optional -->
            <Addr3></Addr3> <!-- optional -->
            <Addr4></Addr4> <!-- optional -->
            <Addr5></Addr5> <!-- optional -->
            <City>Hebron</City> <!-- optional -->
            <State>Kentucky</State> <!-- optional -->
            <PostalCode>41048</PostalCode> <!-- optional -->
            <Country>United States</Country> <!-- optional -->
            <Note>Nice address</Note> <!-- optional -->
        </BillAddress>
        <ShipAddress> <!-- optional -->
            <Addr1>2305 Litton Ln</Addr1> <!-- optional -->
            <Addr2></Addr2> <!-- optional -->
            <Addr3></Addr3> <!-- optional -->
            <Addr4></Addr4> <!-- optional -->
            <Addr5></Addr5> <!-- optional -->
            <City>Hebron</City> <!-- optional -->
            <State>Kentucky</State> <!-- optional -->
            <PostalCode>41048</PostalCode> <!-- optional -->
            <Country>United States</Country> <!-- optional -->
            <Note>Nice address</Note> <!-- optional -->
        </ShipAddress>
        <IsPending>true</IsPending> <!-- optional -->
        <DueDate>2018-03-24T00:31:04+05:00</DueDate> <!-- optional -->
        <Memo>a2e8929f-6f03-4bc2-ad27-ea6aa2cc11cd</Memo> <!-- optional -->
        <InvoiceLineRet> <!-- optional -->
            <TxnLineID>800004ED-1525972764</TxnLineID> <!-- required -->
            <ItemRef> <!-- optional -->
                <ListID>800004ED-1525972764</ListID> <!-- optional -->
                <FullName>Line Haul</FullName> <!-- optional -->
            </ItemRef>
            <Desc>First Line of Invoice</Desc> <!-- optional -->
            <Quantity>1.0</Quantity> <!-- optional -->
            <Rate>500.5</Rate> <!-- optional -->
        </InvoiceLineRet>
        <InvoiceLineRet> <!-- optional -->
            <TxnLineID>800004ED-1525972765</TxnLineID> <!-- required -->
            <ItemRef> <!-- optional -->
                <ListID>800004ED-1525972765</ListID> <!-- optional -->
                <FullName>Fuel Surcharge</FullName> <!-- optional -->
            </ItemRef>
            <Desc>Second Line of Invoice</Desc> <!-- optional -->
            <Quantity>1.0</Quantity> <!-- optional -->
            <Rate>100.5</Rate> <!-- optional -->
        </InvoiceLineRet>
    </InvoiceRet>
    """


@pytest.fixture
def sample_invoice_customer_data():
    return dict(
        ListID='800004ED-1525972764',
        FullName='Amazon',
    )


@pytest.fixture
def sample_invoice_item_service1_data():
    return dict(
        ListID='800004ED-1525972764',
        FullName='Line Haul',
    )


@pytest.fixture
def sample_invoice_item_service2_data():
    return dict(
        ListID='800004ED-1525972765',
        FullName='Fuel Surcharge',
    )


@pytest.fixture
def sample_invoice_line1_data():
    return dict(
        TxnLineID='800004ED-1525972764',
        Desc='First Line of Invoice',
        Quantity=1.0,
        Rate=500.5,
    )


@pytest.fixture
def sample_invoice_line2_data():
    return dict(
        TxnLineID='800004ED-1525972765',
        Desc='Second Line of Invoice',
        Quantity=1.0,
        Rate=100.5,
    )


@pytest.fixture
def sample_invoice_data():
    return dict(
        TxnID='800004ED-1525972764',
        TimeCreated='2018-03-24T00:31:04+05:00',
        TimeModified='2018-03-24T00:31:04+05:00',
        EditSequence='1525972764',
        TxnDate='2018-03-24T00:31:04+05:00',
        IsPending=True,
        DueDate='2018-03-24T00:31:04+05:00',
        Memo='a2e8929f-6f03-4bc2-ad27-ea6aa2cc11cd',
    )


@pytest.fixture()
def xml_compare_fn():
    def remove_whitespaces(xml):
        tree = etree.fromstring(xml)
        root = tree.getroottree()

        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
            if elem.tail is not None:
                elem.tail = elem.tail.strip()
        return root

    def compare(xml1, xml2):
        tree1 = remove_whitespaces(xml1)
        tree2 = remove_whitespaces(xml2)

        assert etree.tostring(tree1, encoding="utf-8", xml_declaration=True) == etree.tostring(tree2, encoding="utf-8", xml_declaration=True)

    return compare
