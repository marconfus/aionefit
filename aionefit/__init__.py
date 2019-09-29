import json
import logging
from .provider.pyaes_impl import AESCipher
from .provider.slixmpp_impl import NefitXmppClient


_LOGGER = logging.getLogger(__name__)

PRODUCT_IDS = {'7746901877': 'Junkers Control CT 100'}


class NefitCore(object):
    _accesskey_prefix = 'Ct7ZR03b_'
    _rrc_contact_prefix = 'rrccontact_'
    _rrc_gateway_prefix = 'rrcgateway_'
    _magic = bytearray.fromhex("58f18d70f667c9c79ef7de435bf0f9b1" +
                               "553bbb6e61816212ab80e5b0d351fbb1")

    container = {}

    def __init__(self, serial_number, access_key, password,
                 host='wa2-mz36-qrmzh6.bosch.de',
                 message_callback=None):
        """Constructor for the NefitCore client.

        :param serial_number:
        :param access_key:
        :param password:
        :param host:
        :param sasl_mech:
        """
        serial_number = str(serial_number)
        self.serial_number = serial_number
        self.password = password
        self.access_key = access_key
        self.message_callback = message_callback

        self.encryption = AESCipher(self._magic, access_key, password)

        identifier = serial_number + "@" + host
        self.jid = self._from = self._rrc_contact_prefix + identifier
        self._to = self._rrc_gateway_prefix + identifier

        _LOGGER.debug('Initializing XMPP client')
        self.xmppclient = NefitXmppClient(jid=self.jid,
                                          password=self._accesskey_prefix +
                                          access_key,
                                          encryption=self.encryption,
                                          nefit_client=self)

    def connect(self):
        self.xmppclient.connect()

    def disconnect(self):
        self.xmppclient.disconnect()

    def raw_message_callback(self, msg):
        if msg['type'] in ('chat', 'normal'):
            headers = msg['body'].split("\n")[:-1]
            body = msg['body'].split("\n")[-1:][0]
            _LOGGER.debug('headers: %s', headers)
            _LOGGER.debug('body: %s', body)
            response = self.encryption.decrypt(body)
            _LOGGER.debug('response: %s', response)

            statusline = headers[0]
            statuscode = statusline.split(" ")[1]
            if statuscode == "204":
                _LOGGER.debug('Empty message (204 No Content) received')

            elif statuscode == "200":
                try:
                    data = json.loads(response)
                    if self.message_callback:
                        self.message_callback(data)
                except json.decoder.JSONDecodeError as e:
                    _LOGGER.error('Error parsing message %s', msg)
                    _LOGGER.error(e)
                    return
            else:
                _LOGGER.error("Errormessage received: %s", statusline)
                if response:
                    _LOGGER.error(response)
                else:
                    _LOGGER.error("response is null")
                raise SystemError(statusline)

    def get(self, path):
        """Construct a "GET command"

        cmd -- the command to send
        """
        msg = 'GET %s HTTP/1.1\rUser-Agent: NefitEasy\r\r' % path
        _LOGGER.debug('Sending msg...%s', msg.replace("\r", "\\r"))

        # dirty hack that is necessary
        msg = msg.replace("\r", "&#13;\n")
        self.xmppclient.send_message(mto=self._to, mbody=msg)

    def put(self, path, data):
        encrypted_data = self.encryption.encrypt(data)
        body = 'PUT %s HTTP/1.1\r' % path + \
               'Content-Type: application/json\r' + \
               'Content-Length: %i\r' % len(encrypted_data) + \
               'User-Agent: NefitEasy\r\r' + \
               '%s' % encrypted_data.decode('utf-8')
        self.xmppclient.send_message(mto=self._to, mbody=body)

    def put_value(self, path, value):
        # For string values, there a space after the : is not allowed
        data = json.dumps({'value': value}, separators=(',', ':'))
        _LOGGER.debug("PUT %s : %s", path, data)
        self.put(path, data)

    def set_usermode(self, mode):
        self.put_value('/heatingCircuits/hc1/usermode', mode)

    def set_temperature(self, temperature):
        t = float(temperature)
        self.put_value('/heatingCircuits/hc1/temperatureRoomManual', t)
        self.put_value('/heatingCircuits/hc1/manualTempOverride/status', 'on')
        self.put_value('/heatingCircuits/hc1/manualTempOverride/temperature',
                       t)
