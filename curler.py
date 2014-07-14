#the driver program to run the app details miner
#will be updating as and when i write new code

import os, sys
from appMiner import mineApps
#from config import PROD_PORT, DEFAULT_PORT, AUTH_CODE
#from app import app as app_table


def extract_app_details():
	#give a URL from where you will fetch the details.
	mainURL = "https://play.google.com"

	#create an initial object for the page
	pager = mineApps(mainURL)

	#create a page detailer object for accessing urls present in main page
	status , pagerObj = pager.fetch_page_details()

	#fetch all the URLs listing app details present in the parent page
	status , app_urls = pager.fetch_app_url(pagerObj)

	#fetch the urls of apps from a search.
	#this will list the app searched for and also fetch data from all related apps
	#just remove comment when you want this to work
	#searchString = ["zombies", "vs", "plants"]
	#status, app_urls = pager.fetch_related_app_details(searchString)

	#fetch the details of each object
	for url in app_urls : 
		status , details = pager.fetch_app_details(url)
		if status == 0 :
			#we can add the db add code here.
			#addStatus, message = app_table.add_app(jsonObj["package_name"],jsonObj["app_name"],jsonObj["developer_id"],jsonObj["app_icon_url"],jsonObj["description"], jsonObj["app_id"], jsonObj["app_rating"], jsonObj["app_category"], jsonObj["app_downloads"])
			print details
		else :
			print "NOT ABLE TO FETCH THE REQUIRED DETAIL"



if __name__ == '__main__':
	extract_app_details()