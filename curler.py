#the driver program to run the app details miner

import os, sys
from appMiner import mineApps



def extract_app_details():
	#give a URL from where you will fetch the details.
	mainURL = "https://play.google.com"
	#create an initial object for the page
	pager = mineApps(mainURL)
	#create a page detailer object for accessing urls present in main page
	status , pagerObj = pager.fetch_page_details()
	#fetch all the URLs listing app details present in the parent page
	status , app_urls , see_more_urls = pager.fetch_app_url(pagerObj, True)

	url = "https://play.google.com/store/apps/details?id=com.king.candycrushsaga"
	status , details = pager.fetch_app_details(url)
	'''
	#fetch the details of each object if there are multiple app urls
	for url in app_urls : 
		status , details = pager.fetch_app_details(url)
		if status == 0 :
			#we can add the db add code here.
			#addStatus, message = app_table.add_app(jsonObj["package_name"],jsonObj["app_name"],jsonObj["developer_id"],jsonObj["app_icon_url"],jsonObj["description"], jsonObj["app_id"], jsonObj["app_rating"], jsonObj["app_category"], jsonObj["app_downloads"])
			print details
		else :
			print "NOT ABLE TO FETCH THE REQUIRED DETAIL"
	'''


if __name__ == '__main__':
	extract_app_details()
