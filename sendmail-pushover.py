#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import stdin
import email
from pushover import Client

pushover_user = os.environ('PUSHOVER_USER')
pushover_api_token = os.environ('PUSHOVER_API_TOKEN')

mail = email.message_from_string(stdin.read())
title = "Message from Sendmail-Pushover"
if "Subject" in mail:
    title = mail['Subject']

client = Client(pushover_user, api_token=pushover_api_token)
client.send_message(mail.as_string(), title=title)
