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
prompt = "> "
filepaths = []
searchID = "empty"
searchcollection = "empty"
testfile = "C:\\Users\\dchan\\Documents\\Abbvie\\Humira\\Old_refs\\testpdf.pdf"
archive = "C:\\Users\\dchan\\Documents\\test.zip"
ziplocation = "C:\\Program Files\\7-Zip\\7zG.exe"

#connect to zotero
print ("\n To login to zotero we'll be using login information stored in: \n\n \t %s \n" % (login_file))
zot = zotero.Zotero(library_id, library_type, apikey)

#retrieve the collections
collections = zot.collections()

#Ask for the search collection
print ("Please enter the collection you want to export")
searchcollection = input(prompt)

#find the collectionID for the specified collection
while searchID == "empty":
    for item in collections:
        if item['data']['name'] == searchcollection:
            searchID = item['data']['key']
    if searchID == "empty":
        print ("\n could not find %s in the zotero library \n reenter the collection \n" % (searchcollection))
        searchcollection = input(prompt)
#    else:
#        print ("D'oh! some other error")

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
print ("\n %d references from the %s collection (%s) have been retrived and zipped into \n\n \t %s" % (len(filepaths), searchcollection, searchID, archive))
