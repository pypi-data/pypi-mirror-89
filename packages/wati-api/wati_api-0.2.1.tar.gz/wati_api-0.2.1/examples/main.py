# Copyright (c) 2020 kien@clare.ai.
# All Rights Reserved.

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import json
import hashlib

from wati_api import client

if __name__ == '__main__':
    try:
        endpoint = os.environ['WATI_API_ENDPOINT']
        token = os.environ['WATI_API_TOKEN']
    except KeyError as e:
        print('Missing environment variables! %s' % str(e))
        raise e
    wa_client = client.Client(endpoint, token)
    print("# Get message API")
    print(wa_client.get_messages("919920842422"))
    print("# Get message templates API")
    print(wa_client.get_message_templates())
    print("# Get contact list API")
    print(wa_client.get_contacts())
    # Need to recheck - 404
    # print("# Get media API")
    # print(wa_client.get_media('ABC'))
    print("# Add contact API")
    custom_params = [
        {
            "name": "member",
            "value": "VIP"
        }
    ]
    print(wa_client.add_contact("919920842422", "ABC", custom_params))
    print("# Update contact attribute")
    print(wa_client.update_contact_attributes("919920842422", custom_params))
    print("# Send Session message")
    print(wa_client.send_session_message("919920842422", "Hello"))
    template_parameters = [
        {
            'name': 'name',
            'value': 'John'
        },
        {
            'name': 'ordernumber',
            'value': '12345'
        }
    ]
    print("# Send template message API")
    print(wa_client.send_template_message(
        whatsapp_number="919920842422",
        broadcast_name="order_update",
        template_name="order_update",
        template_parameters=template_parameters
    ))
