#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'getUsernames' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts INTEGER threshold as parameter.
#
# URL for cut and paste
# https://jsonmock.hackerrank.com/api/article_users?page=<pageNumber>
#

import aiohttp
from aiohttp import web
import datetime
import traceback
import json


# It would be good to use a class... But globals!
PORT: int       = 8080
THRESHHOLD: int = 5
ENDPOINT: str   = '/api/article_users'      # Endpoint of the API
ROWSONPAGE: int = 1                         # For paginating


def srcArr():
    """
        Original data
    """

    arr = [
        {
            'id': 1,
            'username': 'Us1',
            'about': 'Something ab us1',
            'submitted': 4,
            'updated_at': datetime.datetime.now(),
            'submission_count': 4,    # ...approved
            'comment_count': 331,
            'created_at': datetime.datetime.now(),
        },{
            'id': 2,
            'username': 'Us2',
            'about': 'Something ab us2',
            'submitted': 10,
            'updated_at': datetime.datetime.now(),
            'submission_count': 8,    # ...approved
            'comment_count': 6545,
            'created_at': datetime.datetime.now(),
        },{
            'id': 3,
            'username': 'Us3',
            'about': 'Something ab us3',
            'submitted': 15,
            'updated_at': datetime.datetime.now(),
            'submission_count': 45,    # ...approved
            'comment_count': 3434,
            'created_at': datetime.datetime.now(),
        },
    ]

    return arr

def resData():
    """
        Gen result data
    """

    global THRESHHOLD

    lres = []
    for item in srcArr():
        if item['submitted'] > THRESHHOLD:
            lres.append(item)

    return lres

def formPage(indata, curpage):
    """
        Fragement data for paginating
        :indata: -
        :curpage: - ...from 1
    """

    global ROWSONPAGE

    ltotal: int = len(indata)
    ltotalpages: int = ltotal // ROWSONPAGE
    ltotalpages = ltotalpages if ltotal % ROWSONPAGE == 0 else ltotalpages + 1

    lres = indata[(curpage - 1) * ROWSONPAGE:(curpage) * ROWSONPAGE]

    return (ltotal, ltotalpages, lres)

def httpGetHndl(request):
    """
        Get-handler
    """

    global ROWSONPAGE

    lparams = request.rel_url.query

    curpage = lparams.get('page')
    try:
        curpage = int(curpage)
    except Exception as ex:
        curpage = 1

    (ltotal, ltotalpages, ldata) = formPage(resData(), curpage)

    lresj = {
        'page': curpage,
        'per_page': ROWSONPAGE,
        'total': ltotal,
        'total_pages': ltotalpages,
        'data': ldata,

    }

    lres = json.dumps(lresj, indent=4, default=str)

    return aiohttp.web.json_response(text=lres)


def getUsernames(threshold):
    """
        Main
    """

    global PORT
    global ENDPOINT
    global THRESHHOLD
    THRESHHOLD = threshold

    lweb = aiohttp.web
    lapp = lweb.Application()
    # lapp.on_startup.append(on_startup)
    # lapp.on_shutdown.append(on_cleanup)
    # lapp.on_cleanup.append(on_cleanup)
    # lapp.on_shutdown.append(on_shutdown)
    lapp.add_routes([aiohttp.web.get(ENDPOINT, httpGetHndl)])
    try:
        lweb.run_app(lapp, port=PORT)
        print('Started...')
    except Exception as ex:
        print('General error: {}\n{}'.format(ex, traceback.format_exc))



if __name__ == '__main__':
    getUsernames(THRESHHOLD)
