import requests
_PRODUCT_URL = "https://api-v2.gigatron.rs/core/product/index/{}"
_NAVIGATION_MENU = "https://api-v2.gigatron.rs/core/navigation/menu/1"
_CATEGORY_URL = "https://search.gigatron.rs/v1/catalog/get{}"
_CATEGORY_URL_PAGE = "https://search.gigatron.rs/v1/catalog/get{}?page={}"

"""
https://api-v2.gigatron.rs/core/subcategory/get//gaming/konzole-za-igranje?uid=giga5f48d1257a5e34.14322842
https://search.gigatron.rs/v1/catalog/get/gaming/konzole-za-igranje?poredak=rastuci
https://search.gigatron.rs/v1/catalog/get/prenosni-racunari/laptop-racunari?poredak={}&strana={}
"""
def get_product(id):
	return requests.get(_PRODUCT_URL.format(id)).json()["items"]

def get_main_categories():
	json_menu = requests.get(_NAVIGATION_MENU.format()).json()
	return {menu["link"]:menu["title"] for menu in json_menu}

def get_sub_categories():
	subcategories = {}
	json_menu = requests.get(_NAVIGATION_MENU).json()
	for menu in json_menu:
		for key in menu["items"]:
			for submenu in menu["items"][key]:
				subcategories[submenu["link"]] = submenu["title"]
	return subcategories

def get_prod_in_cat(subcat):
	requests.get(_CATEGORY_URL.format())

def get_products_in_subcategory(subcategory_url):
	return requests.get(_CATEGORY_URL.format(subcategory_url)).json()

def get_number_of_products_in_subcategory(subcategory_url):
	return requests.get(_CATEGORY_URL.format(subcategory_url)).json()["hits"]["total"]

"""
import gigatron
from pprint import pprint

pprint(gigatron.get_sub_categories())


print(gigatron.get_number_of_products_in_category("/oprema-za-racunare/mrezna-oprema/nas-uredjaji-i-oprema"))
"""

"""
import pprint
pprint.pprint(get_sub_categories())
"""