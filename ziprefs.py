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

#set variables, defaults to some test files
filepaths = []
serachID = "empty"
searchcollection = "Baseline_characteristics"
testfile = "C:\\Users\\dchan\\Documents\\Abbvie\\Humira\\Old_refs\\testpdf.pdf"
archive = "C:\\Users\\dchan\\Documents\\Abbvie\\Humira\\Old_refs\\test.zip"
ziplocation = "C:\\Program Files\\7-Zip\\7zG.exe"

#connect to zotero
zot = zotero.Zotero(library_id, library_type, apikey)

#retrieve the collections
collections = zot.collections()

#We assume that the search term has been specified as the first argument on the command line
searchcollection = sys.argv[1]
archive = sys.argv[2]

#find the collectionID for the specified collection
for item in collections:
    if item['data']['name'] == searchcollection:
        searchID = item['data']['key']
if searchID == "empty":
    print ("could not find %s in the zotero library" % (searchcollection))
	
#get the items corresponding to the collectionID
collectionsitems = zot.collection_items(searchID)

#get the path to the files for the items which are linked items
for item in collectionsitems:
    if item['data'].get('linkMode') == "linked_file":
	    filepaths.append(item['data'].get('path'))
	
#zip up the filepaths
for path in filepaths:
    subprocess.run("\"%s\" a \"%s\" \"%s\"" % (ziplocation, archive, path),stdout=subprocess.PIPE)
	
#sanity check
print ("%d references from the %s collection (%s) have been retrived and zipped into \n %s" % (len(filepaths), searchcollection, searchID, archive))
