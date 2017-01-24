from pyzotero import zotero
import importlib.util
import sys
import subprocess

#this is where zotero login lives on your computer
login_file = "C:\\Users\\dchan\\Documents\\KEYS\\zoterologin.py"

#this is using the import library to set the path to the module and the module name
spec = importlib.util.spec_from_file_location("zoterologin", login_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

#map the module to sys
sys.modules["zoterologin"] = module

#import the login information
from zoterologin import apikey, library_id, library_type

#set variables

testfile = "C:\\Users\\dchan\\Documents\\Abbvie\\Humira\\Old_refs\\testpdf.pdf"
testarchive = "C:\\Users\\dchan\\Documents\\Abbvie\\Humira\\Old_refs\\test.zip"
ziplocation = "C:\\Program Files\\7-Zip\\7zG.exe"

#connect to zotero
zot = zotero.Zotero(library_id, library_type, apikey)

#retrieve the collections
collections = zot.collections()

#We assume that the search term has been specified as the first argument on the command line
searchcollection = sys.argv[1]

#find the collectionID for the specified collection
for item in collections:
    if item['data']['name'] == searchcollection:
	    searchID = item['data']['key']

#get the items corresponding to the collectionID
collectionfiles = zot.collection_items(searchID)

#get the path to the files for the items
collectionfiles

#Search!
results = zot.top(limit = term)

#How many results are there?
print ("%d results for %s" % (len(results), term))

#Loop through the results and print the item type and ID
for item in results:
    print("Item Type: %s | Key: %s" % (item['data']['itemType'], item['data']['key']))
	
#test zip
subprocess.run("\"%s\" a \"%s\" \"%s\"" % (ziplocation, testarchive, testfile),stdout=subprocess.PIPE)