class SiteMapLocators:
	title = "span.site-map-section-title"
	site_map_sections = 'div.site-map-section'
	site_map_item_title = "a.site-map-item.title"
	site_map_items = "a.site-map-item"
	site_map_categories = 'div.site-map-category'


class ProductPageLocators:
	product_name: str = 'h1[itemprop="name"].product-name'
	description: str = 'p[itemprop="description"].product-info-text'
	# color_options
	product_colors: str = 'div.product-colors'
	colors_info: str = 'div.colors-info'
	colors_img: str = 'div#colorsContainer img'
	#	
	size_options: str = 'div.selector-list span.size-available'
	product_prices: str = 'div[itemprop="offers"].product-prices'
	product_sale: str = 'span.product-sale'
	product_sku: str = 'span[itemprop="mpn"].product-reference'
	seo: str = 'meta[name="description"]'
	images = 'div#renderedImages img'
	tag_elements = 'div.product-info-block li[itemprop="itemListElement"]'