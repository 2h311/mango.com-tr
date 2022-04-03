import time
from random import randint
from pprint import pprint
from typing import Dict, Any

from playwright.sync_api import sync_playwright

from locators import ProductPageLocators, SiteMapLocators
from loggers import *


def sleep(secs: int = randint(1, 5)) -> None:
	producer_logger.info(f"Snoozing {secs} seconds")
	time.sleep(secs)


def get_text(element: object) -> str:
	# a helper function - sift, strip text_content() of page element
	return element.text_content().strip() if element else ''


def get_sub_categories(categories: Dict, site_map_category: object) -> None:
	''' Sub-categories - Giyim, Aksesuarlar '''
	title = get_text(site_map_category.query_selector(SiteMapLocators.title))
	categories[title] = dict()
	producer_logger.debug(f"Grabbing sub-categories for Category -> {title}")
	# grab sub-categories under title/categories 
	site_map_sections = site_map_category.query_selector_all(SiteMapLocators.site_map_sections)

	for site_map_section in site_map_sections:
		# grab the text for the sub-categories
		site_map_item_title = site_map_section.query_selector(SiteMapLocators.site_map_item_title)
		site_map_item_title = get_text(site_map_item_title)
			
		# grab all hrefs of items under each sub-categories
		site_map_items = site_map_section.query_selector_all(SiteMapLocators.site_map_items)[1:]
		site_map_items_dict = dict()
		
		for site_map_item in site_map_items:
			site_map_items_dict[get_text(site_map_item)] = site_map_item.get_attribute('href')
		
		# add the dict holding the sub-categories and their hrefs
		categories[title][site_map_item_title] = site_map_items_dict


def get_categories() -> Dict:
	''' Categories - Kadin, Erkek, Teen, Cocuk '''
	categories = dict()
	producer_logger.debug("Getting SiteMap Categories")
	# site map category elements
	site_map_categories = page.query_selector_all(SiteMapLocators.site_map_categories)
	producer_logger.debug("SiteMap Categories Found")
	producer_logger.debug("Traversing SiteMap Categories")
	for site_map_category in site_map_categories:
		get_sub_categories(categories, site_map_category)
	return categories


def traverse_sitemap() -> None:
	sitemap_url: str = f"{base_url}/tr/sitemap"
	# traverse the sitemap url
	producer_logger.info(f"Going to {sitemap_url}")
	page.goto(sitemap_url)
	categories = get_categories()
	return categories


def get_products_href(count: int = 0) -> None:
	# while True:
	products = page.query_selector_all('li[id*="product-key-id"]')
	current_number_of_products = len(products)
	# if count < current_number_of_products:
	for product in products[count:10]:
		product.scroll_into_view_if_needed()
		href = product.query_selector('a').get_attribute('href')
		products_hrefs.add(href)
		producer_logger.debug(f"Found -> {href}")
		count += 1
	# else:
	# 	break
	# wait some seconds for product list to update
	sleep()


def set_category(category: str, product: Dict) -> None:
	producer_logger.debug(category)
	product['Category'] = category


def set_sub_category(subcategory: str, product: Dict) -> None:
	producer_logger.debug(subcategory)
	product['Sub Category'] = subcategory


def get_name(product: Dict) -> None:
	# product name
	product_name = get_text(page.wait_for_selector(ProductPageLocators.product_name))
	producer_logger.debug(product_name)
	product['Name'] = product_name


def join_collection(collection: Any) -> str:
	''' helper function '''
	if isinstance(collection, dict):
		return '\n\n'.join([f"{key}:{collection.get(key)}" for key in collection ])
	elif isinstance(collection, list):
		return '\n\n'.join(collection)


def get_description(product: Dict) -> None:
	# description
	product_info_block = page.query_selector_all('div.product-info-block')
	description = dict()
	for block in product_info_block:
		product_info_title = get_text(block.query_selector('h2.product-info-title')) 
		product_info_text = get_text(block.query_selector('p.product-info-text'))  
		description[product_info_title] = product_info_text
	producer_logger.debug(description)
	product['Description'] = join_collection(description)


def get_colors(product: Dict) -> None:
	# color option
	product_colors = page.query_selector(ProductPageLocators.product_colors)
	colors_info = product_colors.query_selector_all(ProductPageLocators.colors_info)
	colors_img = product_colors.query_selector_all(ProductPageLocators.colors_img)
	color_option = { get_text(key): value.get_attribute('src') for key, value in zip(colors_info, colors_img) } 
	producer_logger.debug(color_option)
	product['Color'] = join_collection(color_option)


def get_size(product: Dict) -> None:
	# size option
	size_options = page.query_selector_all(ProductPageLocators.size_options)
	# size_option = [ {get_text(size): size.get_attribute('data-value')} for size in size_options ]
	size_option = [ f"{get_text(size)}:{size.get_attribute('data-value')}" for size in size_options ]
	producer_logger.debug(size_option)
	product['Size'] = join_collection(size_option)


def get_prices(product: Dict) -> None:
	product_prices = page.query_selector(ProductPageLocators.product_prices)
	
	sale_price = get_text(product_prices.query_selector(ProductPageLocators.product_sale))
	product['Sale Price'] = sale_price
	sale_percentage = get_text(product_prices.query_selector('span.product-discount')) 
	product['Sale Percentage'] = sale_percentage
	original_price = get_text(product_prices.query_selector('span.product-sale--cross'))
	product['Original Price'] = original_price


def get_sku(product: Dict) -> None:
	# product SKU
	product_sku = get_text(page.query_selector(ProductPageLocators.product_sku))
	producer_logger.debug(product_sku) 
	product['SKU'] = product_sku


def get_seo(product: Dict) -> None:
	# SEO
	seo = page.query_selector(ProductPageLocators.seo).get_attribute('content').strip()
	producer_logger.debug(seo)
	product['SEO'] = seo


def get_images(product: Dict) -> None:
	# product images
	images = page.query_selector_all(ProductPageLocators.images)
	product_images = [ f"https:{image.get_attribute('src')}" for image in images ]
	producer_logger.debug(product_images)
	product['Images'] = join_collection(product_images)


def get_tags(product: Dict) -> None:
	# product tags
	tag_elements = page.query_selector_all(ProductPageLocators.tag_elements)
	product_tags = [ get_text(tag) for tag in tag_elements ] 
	producer_logger.debug(product_tags)
	product["Tags"] = join_collection(product_tags)


def get_product(url: str) -> None:
	product = dict()
	product_url = f"{base_url}{url}"
	page.goto(product_url)

	product['Product URL'] = product_url
	set_category(category, product)
	set_sub_category(sub_category, product) 
	sleep()
	get_name(product); get_description(product)
	get_colors(product); get_size(product)
	get_prices(product); get_sku(product)
	get_seo(product); get_images(product)
	get_tags(product); pprint(product)


base_url = "https://shop.mango.com"

timeout = 45 * 1000

playwright = sync_playwright().start() 
browser = playwright.chromium.launch(headless=False)
context = browser.new_context()
context.set_default_timeout(timeout)
context.set_default_navigation_timeout(timeout)
page = context.new_page()

categories = traverse_sitemap()

category = 'Kadin'
kadin = categories[category]

sub_category = 'Giyim'
giyim = kadin[sub_category]
sub_sub_cat = giyim['Elbise ve tulum']

sub_sub_cat_page = f"{base_url}{sub_sub_cat}"
page.goto(sub_sub_cat_page)
page.wait_for_selector('li[id*="product-key-id"]')

products_hrefs = set()
get_products_href()

for url in products_hrefs:
	get_product(url)