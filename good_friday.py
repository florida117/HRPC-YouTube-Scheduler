import os
import sys
import pickle
import time
import pytz
import calendar
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from googleapiclient.http import MediaFileUpload

import logging
logging.basicConfig(level=logging.INFO)

def EasterSunday(int year)
{
    day = 0;
    month = 0;

    g = year % 19;
    c = year / 100;
    h = (c - (int)(c / 4) - (int)((8 * c + 13) / 25) + 19 * g + 15) % 30;
    i = h - (int)(h / 28) * (1 - (int)(h / 28) * (int)(29 / (h + 1)) * (int)((21 - g) / 11));

    day   = i - ((year + (int)(year / 4) + i + 2 - c + (int)(c / 4)) % 7) + 28;
    month = 3;

    if day > 31; then
    
        month++;
        day -= 31;
    fi

    return new DateTime(year, month, day);
}