from os import getenv
import pandas as pd


__username__ = getenv('SOPHIA_USER')
__password__ = getenv('SOPHIA_PASS')


def set_credentials(_username="guest", _password="guest"):
    global username, password
    __username__ = _username
    __password__= _password

def load_dataset():
		data = {'id':[1,2], 
'country':['chile','france'],
'media_outlet':['latercera','mediapart'], 'url':['www','www'], 
'title':['un titulo','un titre'], 
'text':['un texto','un texte'], 
'date':['2020-01-01','2020-01-02']}
		df = pd.DataFrame(data=data)
		return df

#save on js? as parameter of load or another function especially for download?
if not __username__: set_credentials()