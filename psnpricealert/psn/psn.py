import sys
import logging
from psnpricealert.utils import utils
import time

apiRoot = "https://store.sonyentertainmentnetwork.com/store/api/chihiro/00_09_000"
fetchSize = "99999"
apiVersion = "19"

version = sys.version_info[0]

logging.basicConfig(
    filename="psn.log",
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)-8s] %(message)s",
    filemode = "w")


# import only once
if version == 3:
    from urllib.request import urlopen
    from urllib.parse import quote
elif version == 2:
    from urllib2 import urlopen
    from urllib2 import quote
else:
    version == False

def getItemForCid(cid, store):
    url = apiRoot + "/container/"+store+"/"+apiVersion+"/"+cid+"?size="+fetchSize
    data = utils.getJsonResponse(url)
    return data

def getPrice(item):
    return float(item['default_sku']['price'])/100

def getPlaystationPlusPrice(item):

    rewards = item['default_sku']['rewards']

    for reward in rewards:
        print(utils.prettyPrintJson(reward))
        if (reward['isPlus'] == True):
            return float(reward['price'])/100

    return getPrice(item)

def getCidForName(name, store):

    links = searchForItemsByName(name, store)
    cids = []

    for link in links:
        try:
            logging.debug("Parsing:\n" + utils.prettyPrintJson(link))
            name = link['name']
            itemType = link['default_sku']['name']
            cid = link['default_sku']['entitlements'][0]['id']
            platform = link['playable_platform']
        
            logging.info ("Found: " + name + " - " + cid + " - Platform: " + str(platform) + " - Type: " + itemType)
            cids.append(cid)
        except Exception as e:
            logging.warn("Got error '"+str(e)+"'' while parsing\n" + utils.prettyPrintJson(link))

    return cids

def searchForItemsByName(name, store):
    # encode name for HTTP request
    encName = quote(name)

    url = apiRoot+"/bucket_search/"+store+"/"+apiVersion+"/"+encName+"?size="+fetchSize+"&start=0"
    data = utils.getJsonResponse(url)
    links = data['categories']['games']['links']
    return links

def getItemsByContainer(container, store):

    encContainer = quote(container)
    timestamp = timestamp = int(time.time())
    
    url = apiRoot+"/container/"+store+"/"+apiVersion+"/"+container+"/"+str(timestamp)+"?size="+fetchSize

    data = utils.getJsonResponse(url)
    links = data['links']

    return links
