from pygnotero import libzotero
import sys

#this is where zotero lives on your computer
zotero_folder = "C:\Users\dchan\AppData\Local\Zotero Standalone\"

#connect to zotero
zotero = libzotero.libzotero(zotero_folder)

#We assume that the search term has been specified as the first argument on the command line
term = sys.argv[1]

#Search!
results = zotero.search(term)

#How many results are there?
print "%d results for %s" % (len(results), term)

#Loop through the results and print them in simple format. libzotero.search() returns a list of zotero_item objects. (For more information about the zotero_item class, see pygnotero.zotero_item in the source code.)
for item in results:
    print item.simple_format()