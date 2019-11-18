# -*- coding: utf-8 -*-

import os

TOKEN = os.environ['TOKEN']

ADMIN_DM_CHANNEL = int(os.environ['ADMIN_DM_CHANNEL'])
ACCEPT_LIST_CHANNEL = int(os.environ['ACCEPT_LIST_CHANNEL'])

DB_ACCOUNT = {
    'host': os.environ['POSTGRES_HOST'],
    'db': os.environ['POSTGRES_DB'],
    'user': os.environ['POSTGRES_USER'],
    'password': os.environ['POSTGRES_PASSWORD']
}

REGISTER_CHANNELS = {
    os.environ['SOLO_CHANNEL']: {'name': '2019/12/01 個人応募制', 'type': 'solo'},
    os.environ['TEAM5_CHANNEL']: {'name': '2019/12/01 5人応募制', 'type': 'team5'},
}
