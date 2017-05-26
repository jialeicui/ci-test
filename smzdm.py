#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import sys
import requests
import re

SMZDM_USERNAME = os.getenv('USERNAME')
SMZDM_PASSWORD = os.getenv('PASSWORD')

class SMZDMDailyException(Exception):
    def __init__(self, req):
        self.req = req

    def __str__(self):
        return str(self.req)

class SMZDMDaily(object):
    BASE_URL = 'http://zhiyou.smzdm.com'
    LOGIN_URL = BASE_URL + '/user/login/ajax_check'
    CHECKIN_URL = BASE_URL + '/user/checkin/jsonp_checkin'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def checkin(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'http://www.smzdm.com/'
        }

        params = {
            'username': self.username,
            'password': self.password,
        }

        r = self.session.get(self.BASE_URL, headers=headers, verify=False)
        r = self.session.post(self.LOGIN_URL, data=params, headers=headers, verify=False)
        r = self.session.get(self.CHECKIN_URL, headers=headers, verify=False)
        if r.status_code != 200:
            raise SMZDMDailyException(r)

        data = r.text
        jdata = json.loads(data)

        return jdata

if __name__ == '__main__':
    if SMZDM_USERNAME is '' or SMZDM_PASSWORD is '':
        sys.exit()
    smzdm = SMZDMDaily(SMZDM_USERNAME, SMZDM_PASSWORD)
    result = smzdm.checkin()
