#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os, sys
import re, requests
from urllib import urlencode 

__author__ = 'Radek Dejnek <radek.dejnek@gmail.com>'
__version__ = '1.0'

from error_codes import error_codes
from methods import methods

md5pattern = re.compile('^[0-9A-Fa-f]{32}$')

class ResponseError(Exception):
    pass

class SMSApi(object):
    """Simple SMSAPI implementation"""

    def __init__(self, username, password, _from = None):
        super(SMSApi, self).__init__()

        if not md5pattern.match(password):
            raise ValueError(error_codes['1192']) #md5 error

        self.username = username
        self.password = password

        self._from = _from

        self.global_params = {'username': self.username, 'password': self.password}
        if self._from:
            self.global_params['from'] = self._from

        #get the current points
        self._points = self.points()

    def _binary_converter(message, url = ''):
        """
        Binary (?) converter from smsapi.pl # http://www.smsapi.pl/en/sms-api/tools
        """
        return ('\x86\x06\x01\xae\x02\x05j\x00E\xc6\x0c\x03' + url + '\x00\x07\x01\x03' + message + '\x00\x01\x01').encode('hex')
    def _vcard_converter(first_name, last_name, telephone, email = '', www = ''):
        """
        Binary (?) vcard from smsapi.pl # http://www.smsapi.pl/en/sms-api/tools
        """
        vcard = 'BEGIN:VCARD\r\nVERSION:2.1\r\n'
        vcard += 'FN:' + first_name + ' ' + last_name + '\r\n'
        vcard += 'N:' + last_name + ';' + first_name + ';;;\r\n'
        vcard += 'TEL;PREF;CELL:' + str(telephone) + '\r\n'
        vcard += 'EMAIL;INTERNET:' + email + '\r\n'
        vcard += 'URL:' + www + '\r\n'
        vcard += 'END:VCARD'
        return vcard.encode('hex')

    def __getattr__(self, method):
        """
        returns list of message ids
        or integer or shit...
        """
        def call(self, **kwargs):
            endpoint = methods[method]

            required_params = endpoint.get('required_params', [])
            valid_params = endpoint.get('valid_params', [])
            if not all( map( lambda x: x in kwargs.keys(), required_params ) ):
                raise KeyError("Required params: %s" % required_params) 

            if 'to' in kwargs and isinstance(kwargs['to'], (list, tuple)):
                kwargs['to'] = ','.join(map(str, kwargs['to'])) # for massive sends..

            if '_from' in kwargs: #python special keyword
                kwargs['from'] = kwargs['_from']
                del kwargs['_from']

            if method == 'wap_push':
                kwargs['message'] = self._binary_converter(kwargs['message'], kwargs.get('url', ''))

            if method == 'vcard':
                kwargs['message'] = self._vcard_converter(kwargs['first_name'], kwargs['last_name'], kwargs['telephone'], kwargs.get('email', ''), kwargs.get('www', ''))

                del kwargs['first_name'], kwargs['last_name'], kwargs['telephone']
                if 'email' in kwargs:
                    del kwargs['email']
                if 'www' in kwargs:
                    del kwargs['www']

            params = self.global_params.copy()
            params.update(endpoint.get('params', {}))
            params.update(kwargs)

            url = endpoint['url']

            r = requests.post(url, data=params)
            if r.status_code != requests.codes.ok:
                raise r.raise_for_status()

            response = r.text

            #helpers
            def parse_multiple():
                parts = response.split(';')
                for part in parts:
                    code, id, points, phone = part.split(':')
                    if code == 'OK':
                        self._points -= int( float(points) * 10000 )
                        yield id

            def parse_points():
                #<PKT>;<Pro>;<Eco>;<MMS>;<VMS_GSM>;<VMS_STAC>
                pkt, pro, eco, mms, gsm, stac = response[1].split(';')
                pkt = int( float(pkt) * 10000 )
                return {'points': pkt, 'pro':pro, 'eco': eco, 'mms': mms, 'vms_gsm': gsm, 'vms_stac': stac}

            #
            if method == 'send' and ';' in response:
                return list(parse_multiple())

            response = response.split(':')
            if response[0] == 'ERROR':
                raise ResponseError(error_codes[response[1]])

            if method == 'points' and kwargs.get('details'):
                return parse_points()
            if method == 'points':
                return int( float(response[1]) * 10000 )
            if method in ('add_user', 'edit_user', 'user_info', 'users', 'add_sender', 'check_sender_status', 'delete_sender', 'senders_list', 'set_default_sender'):
                if r.headers['Content-Type'].startswith('application/json'):
                    return r.json()
                if not response[1:]:
                    return True
                return response[1:]

            self._points -= int( float(response[2]) * 10000 )
            return response[1]

        if method not in methods:
            raise AttributeError("Method %s not found" % method)
        return call.__get__(self)

if __name__ == '__main__':
    sms = SMSApi('username', 'pssword')
    print sms._points

        