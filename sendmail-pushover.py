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

mail = email.message_from_string(stdin.read())
title = "Message from Sendmail-Pushover"

conn = http.client.HTTPSConnection(f"{pushover_domain}:{pushover_port}")
conn.request("POST", "/1/messages.json",
             urllib.parse.urlencode({
                 "token": pushover_api_token,
                 "user": pushover_user,
                 "message": mail.as_string(),
             }), {"Content-type": "application/x-www-form-urlencoded"})
conn.getresponse()
