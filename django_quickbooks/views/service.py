from spyne.decorator import rpc
from spyne.model.complex import Array, Unicode
from spyne.model.primitive import Integer, String
from spyne.service import ServiceBase

from django_quickbooks import QBWC_CODES, HIGHEST_SUPPORTING_QBWC_VERSION, \
    get_session_manager
from django_quickbooks.signals import realm_authenticated


class QuickBooksService(ServiceBase):

    @rpc(Unicode, Unicode, _returns=Array(Unicode))
    def authenticate(ctx, strUserName, strPassword):
        """
        Authenticate the web connector to access this service.

        @param strUserName user name to use for authentication
        @param strPassword password to use for authentication

        @return the completed array
        """
        print('authenticate()')
        return_array = []
        realm = session_manager.authenticate(username=strUserName, password=strPassword)
        if realm and realm.is_active:
            realm_authenticated.send(sender=realm.__class__, realm=realm)
            if not session_manager.in_session(realm):
                session_manager.add_new_jobs(realm)
                if session_manager.new_jobs(realm):
                    ticket = session_manager.set_ticket(realm)
                    return_array.append(ticket)
                    return_array.append(QBWC_CODES.CC)
                    # TODO: need to think about appropriate management of delays
                    # returnArray.append(str(settings.QBWC_UPDATE_PAUSE_SECONDS))
                    # returnArray.append(str(settings.QBWC_MINIMUM_UPDATE_SECONDS))
                    # returnArray.append(str(settings.QBWC_MINIMUM_RUN_EVERY_NSECONDS))
                else:
                    return_array.append(QBWC_CODES.NONE)
                    return_array.append(QBWC_CODES.NONE)
            else:
                return_array.append(QBWC_CODES.BUSY)
                return_array.append(QBWC_CODES.BUSY)
        else:
            return_array.append(QBWC_CODES.NVU)
            return_array.append(QBWC_CODES.NVU)

        print('authenticate(): authenticated_array=%s' % return_array)
        return return_array

    @rpc(Unicode, _returns=Unicode)
    def clientVersion(ctx, strVersion):
        """
        Evaluate the current web connector version and react to it.

        @param strVersion the version of the QB web connector

        @return string telling the web connector what to do next.
        """

        print('clientVersion(): version=%s' % strVersion)
        # TODO: add version checker for types: warning, error, ok
        return QBWC_CODES.CV

    @rpc(Unicode, _returns=Unicode)
    def closeConnection(ctx, ticket):
        """
        Tell the web service that the web connector is finished with the updated session.

        @param ticket the ticket from web connector supplied by web service during call to authenticate method
        @return string telling the web connector what to do next.
        """
        print('closeConnection(): ticket=%s' % ticket)
        session_manager.clear_ticket(ticket)
        return QBWC_CODES.CONN_CLS_OK

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def connectionError(ctx, ticket, hresult, message):
        """
        Tell the web service about an error the web connector encountered in its attempt to connect to QuickBooks
        or QuickBooks POS

        @param ticket the ticket from web connector supplied by web service during call to authenticate method
        @param hresult the HRESULT (in HEX) from the exception thrown by the request processor
        @param message The error message that accompanies the HRESULT from the request processor

        @return string value "done" to indicate web service is finished or the full path of the different company for
        retrying _set_connection.
        """
        print('connectionError(): ticket=%s, hresult=%s, message=%s' % (ticket, hresult, message))
        session_manager.clear_ticket(ticket)
        return QBWC_CODES.CONN_CLS_ERR

    @rpc(Unicode, _returns=Unicode)
    def getLastError(ctx, ticket):
        """
        Allow the web service to return the last web service error, normally for displaying to user, before
        causing the update action to stop.

        @param ticket the ticket from web connector supplied by web service during call to authenticate method

        @return string message describing the problem and any other information that you want your user to see.
        The web connector writes this message to the web connector log for the user and also displays it in the web
        connector’s Status column.
        """
        print('getLastError(): ticket=%s' % ticket)
        return QBWC_CODES.UNEXP_ERR

    @rpc(Unicode, _returns=Unicode)
    def getServerVersion(ctx, ticket):
        """
        Provide a way for web-service to notify web connector of it’s version and other details about version

        @param ticket the ticket from web connector supplied by web service during call to authenticate method

        @return string message string describing the server version and any other information that user may want to see
        """
        print('getServerVersion(): version=%s' % HIGHEST_SUPPORTING_QBWC_VERSION)
        return HIGHEST_SUPPORTING_QBWC_VERSION

    @rpc(Unicode, _returns=Unicode)
    def interactiveDone(ctx, ticket):
        """
        Allow the web service to indicate to web connector that it is done with interactive mode.

        @param ticket the ticket from web connector supplied by web service during call to authenticate method

        @return string value "Done" should be returned when interactive session is over
        """
        print('interactiveDone(): ticket=%s' % ticket)
        return QBWC_CODES.INTR_DONE

    @rpc(Unicode, Unicode, _returns=Unicode)
    def interactiveRejected(ctx, ticket, reason):
        """
        Allow the web service to take alternative action when the interactive session it requested was
        rejected by the user or by timeout in the absence of the user.

        @param ticket the ticket from web connector supplied by web service during call to authenticate method
        @param reason the reason for the rejection of interactive mode

        @return string value "Done" should be returned when interactive session is over
        """
        print('interactiveRejected()')
        print(ticket)
        print(reason)
        return 'Interactive mode rejected'

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Integer)
    def receiveResponseXML(ctx, ticket, response, hresult, message):
        """
        Return the data request response from QuickBooks or QuickBooks POS.

        @param ticket the ticket from web connector supplied by web service during call to authenticate method
        @param response qbXML response from QuickBooks or qbposXML response from QuickBooks POS
        @param hresult  The hresult and message could be returned as a result of certain errors that could occur when
        QuickBooks or QuickBooks POS sends requests is to the QuickBooks/QuickBooks POS request processor via the
        ProcessRequest call
        @param message The error message that accompanies the HRESULT from the request processor

        @return int a positive integer less than 100 represents the percentage of work completed. A value of 1 means one
        percent complete, a value of 100 means 100 percent complete--there is no more work. A negative value means an
        error has occurred and the Web Connector responds to this with a getLastError call.
        """
        print('receiveResponseXML()')
        print("ticket=" + ticket)
        print("response=" + response)
        if hresult:
            print("hresult=" + hresult)
            print("message=" + message)

        return session_manager.process_response(ticket, response, hresult, message)

    @rpc(Unicode, Unicode, Unicode, Unicode, Integer, Integer, _returns=String)
    def sendRequestXML(ctx, ticket, strHCPResponse, strCompanyFileName, qbXMLCountry, qbXMLMajorVers, qbXMLMinorVers):
        print('sendRequestXML() has been called')
        print('ticket:', ticket)
        print('strHCPResponse', strHCPResponse)
        print('strCompanyFileName', strCompanyFileName)
        print('qbXMLCountry', qbXMLCountry)

        return session_manager.get_request(ticket)

    @rpc(Unicode, Unicode, _returns=Unicode)
    def interactiveUrl(ctx, ticket, sessionID):
        print('interactiveUrl')
        print(ticket)
        print(sessionID)
        return ''


session_manager = get_session_manager()
