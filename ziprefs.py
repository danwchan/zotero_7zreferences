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
confirm = "n"
filepaths = []
foundcount = dict()
noparent = []
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
        print ("\n could not find %s in the zotero library \n reenter the collection" % (searchcollection))
        searchcollection = input(prompt)
#    else:
#        print ("D'oh! some other error")

#get the attachement items corresponding to the collectionID
attachments = zot.everything(zot.collection_items(searchID, itemType='attachment'))

#get the non_attachment items corresponding to the collectionID
otheritems = zot.everything(zot.collection_items(searchID, itemType='-attachment'))

#get the path to the files for the items which are linked items
for item in attachments:
    if item['data'].get('linkMode') == "linked_file":
        filepaths.append(item['data'].get('path'))
        parent = item['data'].get('parentItem')
#track the parent key for each item, if no parent then log
        if not parent:
            noparent.append(item['data'].get('title'))
#create a tally for multiples 
        else:
            foundcount[parent] = foundcount.get(parent, 0) + 1

#sanity check
print ("\n %d files have been found for %d references from the %s collection (%s)" % (len(filepaths), len(otheritems), searchcollection, searchID))
for item, files in foundcount.items():

    if files >= 2:
# the generator function as the first string looks over the otheritems list and gets the title from the key provided by item
        print("\n The reference titled '{0}' has {1} files assocated with it".format(next((i for i in otheritems if i['key'] == item))['data'].get('title'), files))

# a loop to print the items in noparent
print("\n The following files to be added to the zip archive have no parent reference: \n")
for orphan in noparent:
    print(orphan)

#a list and printing for a set of items which do not have files associated with them
print("\n The following references have no associated file to add: \n")
foundlist = [keys for keys, count in foundcount.items()]
for found in [item['data'].get('title') for item in otheritems if item['key'] not in foundlist]:
    print(found)

#Ask for the place to put the files
while confirm != "y":
    fileparts = []
    print ("\n Where would you like to save this .zip file? (dont for get the trailing \)")
    archivepath = input(prompt)
    fileparts.extend([archivepath, searchcollection, "_references.zip"])
    archive = "".join(fileparts)
    print ("You want this file to be saved as: \n\n \t %s \n\n Is that correct? (y/n)" % (archive))
    confirm = input(prompt)
    if confirm == "y":
        break
print ("\n GREAT! let's zip it up")

#zip up the filepaths
for path in filepaths:
    subprocess.run("\"%s\" a \"%s\" \"%s\"" % (ziplocation, archive, path),stdout=subprocess.PIPE)

#sanity check confirmation
print ("\n %d references from the %s collection have been retrived and zipped into \n \t %s" % (len(filepaths), searchcollection, archive))
