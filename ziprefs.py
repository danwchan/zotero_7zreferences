from pyzotero import zotero
import importlib.util
import sys

#this is where zotero login lives on your computer
login_file = "C:\Users\dchan\Documents\KEYS\zoterologin.py"

#this is using the import library to set the path to the module and the module name
spec = importlib.util.spec_from_file_location("zoterologin", login_file)
keyfile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(keyfile)

#import the login information
from keyfile import apikey, library_id, library_type

#set variables


#connect to zotero
zot = zotero.Zotero(library_id, library_type, api_key)

#We assume that the search term has been specified as the first argument on the command line
term = sys.argv[1]

#Search!
results = zot.top(limit = term)

#How many results are there?
print "%d results for %s" % (len(results), term)

#Loop through the results and print the item type and ID
for item in results:
    print('Item Type: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))