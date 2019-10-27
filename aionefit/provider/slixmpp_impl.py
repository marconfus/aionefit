import slixmpp
import asyncio
import logging
from slixmpp.xmlstream import tostring

_LOGGER = logging.getLogger(__name__)


class NefitXmppClient(slixmpp.ClientXMPP):
    """XMPP client implementation using the slixmpp library
    """

    def __init__(self, jid, password, encryption, nefit_client=None):

        slixmpp.ClientXMPP.__init__(self, jid, password,
                                    sasl_mech="DIGEST-MD5")
        self.nefit_client = nefit_client
        # the event signaling, that the connection is established
        self.connected_event = asyncio.Event()
        self.disconnected_event = asyncio.Event()
        self.message_event = asyncio.Event()

        # set the various callback handlers
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('session_end', self.session_end)
        self.add_event_handler('message', self.message_callback)
        self.add_event_handler('carbon_received', self.carbonmsg_recv_callblack)
        self.add_event_handler('carbon_sent', self.carbonmsg_sent_callblack)
        self.add_event_handler('failed_auth', self.on_failed_auth)
        self.add_event_handler('auth_success', self.on_auth_success)
        self.register_plugin('xep_0199') #ping
        self.register_plugin('xep_0280') #carbons
        self.encryption = encryption


    def on_failed_auth(self, event):
        """Callback handler for an unsuccessfull authentication.
        """
        if self.nefit_client.failed_auth_handler:
            self.nefit_client.failed_auth_handler(event)
        else:
            _LOGGER.error('failed_auth event: %s', event)
            raise SystemError('Invalid login. Check credentials ' +
                              '(serial_number, access_key, password).')

    def on_auth_success(self, event):
        """Callback handler for a successfull authentication.
        """
        _LOGGER.debug('auth_success event: %s', event)

    def session_start(self, event):
        """Callback handler for the session start.
        """
        self.send_presence()
        self.get_roster()
        self['xep_0280'].enable()
        self.connected_event.set()

    def session_end(self, event):
        _LOGGER.debug("Connection was closed")

        if self.nefit_client.session_end_callback:
            self.nefit_client.session_end_callback()
            
        self.disconnected_event.set()

    def message_callback(self, msg):
        """Callback handler for a received message.
        """
        self.nefit_client.raw_message_callback(msg)
        self.message_event.set()

    def carbonmsg_recv_callblack(self, msg):
        """Callback handler for a received carbon message.
        """
        self.nefit_client.raw_message_callback(msg['carbon_received'])
        self.message_event.set()

    def carbonmsg_sent_callblack(self, msg):
        """Callback handler for a sent carbon message.
        """
        _LOGGER.debug('Carbon sent: %s', msg['carbon_sent'])

    def send_message(self, mto, mbody, msubject=None, mtype=None,
                     mhtml=None, mfrom=None, mnick=None):

        # wild hack that is necessary
        body = mbody.replace("\r", "&#13;\n")
        message = self.make_message(mto=mto, mfrom=mfrom, mbody=body)
        message['lang'] = None
        str_data = tostring(message.xml, xmlns=message.stream.default_ns,
                            stream=message.stream,
                            top_level=True)
        str_data = str_data.replace("&amp;#13;", "&#13;")
        message.stream.send_raw(str_data)
