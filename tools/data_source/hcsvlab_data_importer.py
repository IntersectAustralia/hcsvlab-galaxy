import sys
import os
import pycurl
import cStringIO
import json
from shutil import copyfile

numFiles = sys.argv[1]
logFile = sys.argv[2]
logFileID = sys.argv[3]
fileDir = sys.argv[4]
itemListURI = sys.argv[5]
api_key = sys.argv[6]
selectedTypes = sys.argv[7]
importMetadata = sys.argv[8]
importIndexable = sys.argv[9]
concatenate = sys.argv[10]		

def api_request(url):
	curl = pycurl.Curl()
	buf = cStringIO.StringIO()
	curl.setopt(curl.URL, url)
	curl.setopt(pycurl.HTTPHEADER, ['X-API-KEY: ' + api_key, 'Accept: application/json'])
	curl.setopt(curl.WRITEFUNCTION, buf.write)
	curl.perform()
	response = buf.getvalue()
	status = curl.getinfo(pycurl.HTTP_CODE)	
	if status == 200:
		return status, response
	else:
		raise Exception("api response ( "+str(status)+"): "+str(response)+"\n")

def get_json(url):
	try: 
		status, string = api_request(url)
		response = json.loads(string)
		return response
	except:
		raise		

def importData(prefix, ext, data):
	prefix = prefix.replace("_", "-")
	newFile = "%s/primary_%s_%s_visible_%s" % (fileDir, logFileID, prefix, ext)
	target = open (newFile, 'w')
	target.write(str(data))
	target.close()

def importDocument(document):
	docURL = document['url']
	listURL = docURL.split("/")
	docName= listURL[-1]
	docPrefix = docName.split(".")[0]
	docExt = docName.split(".")[-1]
	try:
		status, content = api_request( url=(docURL).encode('ascii','ignore'))
		importData(docPrefix, docExt, content)
	except Exception,e:
		#do not exit if a document could not be imported. Just log the details.
		log.write("!! Error importing document "+docURL+": "+ str(e))

documentsList =[]
indexableDocumentsList =[]
metadataList =[]

log = open (logFile, 'a')
log.write("HCS vLab Import Tool.\n\n")
log.write("User input parameters are as follows: \n")
log.write("\t Item List URI: "+itemListURI+"\n")
log.write("\t API-KEY: "+api_key+"\n")
log.write("\t Job Name: "+logFile+"\n")
log.write("\t Import File Types: "+selectedTypes+"\n")
log.write("\t Import Metadata: "+importMetadata+"\n")
log.write("\t Import Indexed Documents: "+importIndexable+"\n")
log.write("\t Concatenate Text Files: "+concatenate+"\n\n")

try:
	itemListResponse = get_json(url=itemListURI)

	#get items
	itemURIs = itemListResponse['items']
	log.write("This item list contains "+str(len(itemURIs))+" items.\n\n")

	for itemURI in itemURIs:
		log.write("---- ITEM: " +str(itemURI) + "\n")
		itemResponse =  get_json(url=(itemURI).encode('ascii','ignore'))
		itemName = (str(itemURI)).split("/")[-1]

		#add the documents/metadata associated with this item
		if importMetadata == "true":
			log.write("metadata document: "+(str(itemResponse['metadata']))[:100]+"...\n")
			metadataItem = {'name':itemName }
			metadataItem['content'] = itemResponse['metadata']
			metadataList.append(metadataItem)
		if importIndexable  == "true" and (str(itemResponse['primary_text_url']) != "No primary text found"):
			log.write("indexable document: "+(str(itemResponse['primary_text_url']))+"\n")
			indexableItem = {'name':itemName}
			indexableItem['url'] = itemResponse['primary_text_url']
			indexableDocumentsList.append(indexableItem)
		else:
			docs = itemResponse['documents']
			for doc in docs: 
				if doc['dc:type'] in selectedTypes:
					log.write("document: "+str(doc['url'])+"\n")
					documentsList.append(doc)
		log.write("\n\n")			

	# TODO: concatenation
		# get every document with 'text' type (remove from list)
		# do concatenation	

	for document in documentsList:
		importDocument(document)
	for indexableItem in indexableDocumentsList:
		status, content = api_request( url=(indexableItem['url']).encode('ascii','ignore'))
		importData(indexableItem['name']+' indexable-document', 'txt', content)	
	for metadataItem in metadataList:
		importData(metadataItem['name']+' metadata-document', 'txt', metadataItem['content'])	

	log.close()
except Exception,e:
    log.write("ERROR: "+str(e)+"\n")
    raise