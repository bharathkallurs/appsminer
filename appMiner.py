import os, sys, re
import urllib2
from bs4 import BeautifulSoup


class mineApps:
	def __init__(self, pagePath):

		self.page = pagePath
		print self.page

	#read the page provided during object creation
	@staticmethod
	def set_buffer(pageURL):
		soup = BeautifulSoup(urllib2.urlopen(pageURL).read())
		return soup

	#set an object for the page given. put the details in that object
	def fetch_page_details(self):
		try :
			pager = mineApps.set_buffer(self.page)
			return (0, pager)

		except Exception as e:
			print sys.exc_info()[0], e
			return (-1, "Not able to fetch page details")

	#fetch all the app id urls from the above url
	def fetch_app_url(self, soup):
		print "m coming inside fetch_app_url"
		try :
			linkArray = []
			hrefVal = '/store/apps/details\?id='
			soup.prettify()
			
			for link in soup.find_all('a', href=re.compile(hrefVal)): #a tag, class name
				if link.get('href') not in linkArray :
					linkArray.append(link.get('href'))
			
			#print linkArray
			return(0, linkArray)
		except Exception as e :
			print sys.exc_info()[0], e
			return(-1, "Not able to fetch app URL")

	#fetch the individual app details.
	def fetch_app_details(self, uri):
		try:
			#puts app_id, developer_id, app_name, app_rating, app_description, app category, app_icon_url
			app_url = ""
			app_id = app_name = app_rating = category = description = app_downloads = app_icon_url = None
			package_name = developer_id = None

			uri.strip()

			if "https://play.google.com" not in uri :
				app_url = "https://play.google.com" + uri
			else :
				app_url = uri

			print app_url

			detailer = mineApps.set_buffer(app_url)
			detailer.prettify()

			#app_id package name
			hrefVal = re.compile('/store/apps/details\?id=')
			app_id = hrefVal.sub('', app_url)
			print app_id

			#developer id
			hrefDev = '/store/apps/developer\?id='
			dev_href= detailer.find('a', href=re.compile(hrefDev))
			devIDURL = re.compile(hrefDev)
			developer_id = devIDURL.sub('', dev_href.get('href'))

			#author_f_name, author_l_name
			developerName = developer_id
			#author_f_name, author_l_name = developerName.split('+')
			
			#app name
			app_name = (detailer.find(itemprop="name", class_="document-title").text).strip()
			
			#app rating
			app_rating = (detailer.find(class_="score").text).strip()

			#app category
			category = ""
			# a bit of dance for games category
			game_cats = ["Action", "Adventure", "Arcade", "Board", "Card", "Casino", "Casual", "Educational", "Family", "Music", "Puzzle", "Racing", "Role Playing", "Simulation", "Sports", "Strategy", "Trivia", "Widgets", "Word"]
			catg = detailer.find(itemprop="genre").text
			if catg in game_cats :
				category = "Games"
			else :
				category = catg

			#app description
			description = detailer.find("div",class_="description").text

			#app icon url
			image = detailer.find(itemprop="image")
			app_icon_url = image["src"]

			#number of downloads
			app_downloads = (detailer.find("div",class_="stars-count").text).strip()

			#return everything packed in a json object
			#this is not a json, i wanted this to be, but again lets see
			jsonString = {
					"app_name" : app_name,
					"app_id" : app_id,
					"package_name": app_id,
					"developer_id": developer_id,
					"app_rating" : app_rating,
					"app_category": category,
					"app_icon_url": app_icon_url,
					"app_downloads": app_downloads,
					"description" : description,
				}

			#if None not in (app_id, app_name, app_rating, category, description, app_downloads, app_icon_url, developer_id) :
			return(0, jsonString)

		except Exception as e:
			print sys.exc_info()[0], e
			return (-1, "Not able to fetch anything from this page")

	#fetch the details of apps in the page in a search result.
	# Ex : search for ingress and fetch details of all apps related to ingress displayed on that page.
	def fetch_related_app_details(self, searchStr):
		try :
			uri = "https://play.google.com/store/search?q="
			searchUrl = uri + '%20'.join(searchStr)
			
			print searchUrl

			searcher = mineApps(searchUrl)
			status, searcherObj = searcher.fetch_page_details()
			status, searchArray = searcher.fetch_app_url(searcherObj)
			
			return (status, searchArray)
		except Exception as e :
			print sys.exc_info()[0], e
			return(-1, "not able to fetch related app details")
			


fetch_page_details = mineApps.fetch_page_details
fetch_app_url = mineApps.fetch_app_url
fetch_app_details = mineApps.fetch_app_details
fetch_related_app_details = mineApps.fetch_related_app_details
