import sys
import os
import pycurl
import cStringIO
import json

numFiles = sys.argv[1]
logFile = sys.argv[2]
logFileID = sys.argv[3]
fileDir = sys.argv[4]
itemListURI = sys.argv[5]
api_key = sys.argv[6]
selectedTypes = sys.argv[7]
importMetadata = sys.argv[8]
concatenate = sys.argv[9]	

#tallies of import successes/fails for logging
importSuccessCount=0
importFailCount=0

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
	try:
		prefix = prefix.replace("_", "-")
		newFile = "%s/primary_%s_%s_visible_%s" % (fileDir, logFileID, prefix, ext)
		target = open (newFile, 'w')
		target.write(str(data))
		target.close()
		global importSuccessCount
		importSuccessCount +=1
	except Exception,e:
		#do not exit if a document could not be imported. Just log the details.
		log.write("!! Error saving document "+prefix+"."+ext+": "+ str(e))
		global importFailCount
		importFailCount += 1

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
		global importFailCount
		importFailCount += 1

documentsList =[]
concatenateList =[]
metadataList =[]

log = open (logFile, 'a')
log.write("HCS vLab Import Tool.\n\n")
log.write("User input parameters are as follows: \n")
log.write("\t Item List URI: "+itemListURI+"\n")
log.write("\t API-KEY: "+api_key+"\n")
log.write("\t Job Name: "+logFile+"\n")
log.write("\t Import File Types: "+selectedTypes+"\n")
log.write("\t Import Metadata: "+importMetadata+"\n")
log.write("\t Concatenate Text Files: "+concatenate+"\n\n")

try:
	itemListResponse = get_json(url=itemListURI)

	#get items
	itemURIs = itemListResponse['items']
	log.write("This item list contains "+str(len(itemURIs))+" items.\n\n")

	for itemURI in itemURIs:
		log.write("ITEM: " +str(itemURI) + "\n")
		itemResponse =  get_json(url=(itemURI).encode('ascii','ignore'))
		itemName = (str(itemURI)).split("/")[-1]

		#collect the documents/metadata to import
		if importMetadata == "true":
			content = itemResponse['metadata']
			log.write("---- metadata document: "+(str(content))[:100]+"...\n")
			metadataItem = {'name':itemName }
			metadataItem['content'] = content
			metadataList.append(metadataItem)
		if concatenate == "true" and (str(itemResponse['primary_text_url']) != "No primary text found"):
			indexableItem = {'name':itemName}
			indexableItem['url'] = itemResponse['primary_text_url']
			concatenateList.append(indexableItem)
		docs = itemResponse['documents']
		for doc in docs: 
			if doc['dc:type'] in selectedTypes:
				log.write("---- document: "+str(doc['url'])+"\n")
				if (concatenate == "false" or doc['dc:type'] != "Text"):
					documentsList.append(doc)
	log.write("\n\n")				

	#perform imports
	for document in documentsList:
		importDocument(document)
	for metadataItem in metadataList:
		content = json.dumps(metadataItem['content'], indent=4)
		importData(metadataItem['name']+' metadata-document', 'txt', content)
	if concatenate=="true":
		concatenatedContent =""
		for textItem in concatenateList:
			try:
				status, content = api_request( url=(textItem['url']).encode('ascii','ignore'))
				concatenatedContent = concatenatedContent +"\n\n"+str(content)
			except Exception, e:
				log.write("!! Error importing document "+str(textItem['url'])+": "+ str(e)+"\n")
		if concatenatedContent != "":
			importData('concatenated texts', 'txt', concatenatedContent)

	#log the results
	log.write(str(importSuccessCount)+" document(s) were successfully imported.\n")
	log.write(str(importFailCount)+" document(s) could not be imported due to errors.\n")
	log.close()

except Exception,e:
    log.write("ERROR: "+str(e)+"\n")
    raise
