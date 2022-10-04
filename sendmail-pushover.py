#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import stdin
import email
import http.client
import urllib

pushover_domain = os.environ.get('PUSHOVER_DOMAIN', 'api.pushover.net')
pushover_port = os.environ.get('PUSHOVER_PORT', '443')
pushover_user = os.environ.get('PUSHOVER_USER')
pushover_api_token = os.environ.get('PUSHOVER_API_TOKEN')

def get_email_body(emailobj):
    """ Return the body of the email, preferably in text.
    """

    def _get_body(emailobj):
        """ Return the first text/plain body found if the email is multipart
        or just the regular payload otherwise.
        """
        if emailobj.is_multipart():
            for payload in emailobj.get_payload():
                # If the message comes with a signature it can be that this
                # payload itself has multiple parts, so just return the
                # first one
                if payload.is_multipart():
                    return _get_body(payload)

                body = payload.get_payload()
                if payload.get_content_type() == "text/plain":
                    return body
        else:
            return emailobj.get_payload()

    body = _get_body(emailobj)

    enc = emailobj["Content-Transfer-Encoding"]
    if enc == "base64":
        body = base64.decodestring(body)

    return body

mail = email.message_from_string(stdin.read())
body = get_email_body(mail)

conn = http.client.HTTPSConnection(f"{pushover_domain}:{pushover_port}")
conn.request("POST", "/1/messages.json",
             urllib.parse.urlencode({
                 "token": pushover_api_token,
                 "user": pushover_user,
                 "message": body,
             }), {"Content-type": "application/x-www-form-urlencoded"})
conn.getresponse()
