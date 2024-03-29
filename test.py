import pandas as pd
import numpy as np
import json
pd.set_option('display.max_columns',None)
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# !pip3 install xls2xlsx
from xls2xlsx import XLS2XLSX
# !pip install gspread
import gspread
import datetime
# !pip3 install sidetable
import sidetable as stb
from IPython.display import clear_output
import shutil
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
today=date.today().strftime("%a-%b-%Y")
yesterday = (date.today()- timedelta(days = 1)).strftime("%Y-%m-%d")
this_year = int(date.today().strftime("%Y"))
last_year = int(this_year)-1
last_last_year = int(this_year)-2
import re
import warnings
warnings.filterwarnings('ignore')
clear_output()

sa = gspread.service_account(filename = 'sibedaspbg-logbook-cab4b99bdcae.json')
sp = sa.open('rekap pbg')

sh = sp.worksheet('Data')

logb = pd.DataFrame(sh.get_all_values()[1:])
logb.columns = sh.get_all_values()[0]
tahuns = []
for tahun, year in zip(logb['TAHUN TERBIT'], logb['Tahun Berjalan']):
    tahuns.append(max(tahun, year))
logb['Tahun'] = tahuns
logb = logb[logb['Tahun']!='']
logb.drop(columns=['2/8','TAHUN TERBIT','Tahun Berjalan'],inplace=True)