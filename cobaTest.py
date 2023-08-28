import pandas as pd
# !pip install gspread
import gspread
import datetime
from IPython.display import clear_output
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