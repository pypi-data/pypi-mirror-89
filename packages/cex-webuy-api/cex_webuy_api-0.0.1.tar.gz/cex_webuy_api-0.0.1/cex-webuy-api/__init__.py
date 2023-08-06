import requests

def get_product_url(product_id):
    return f"https://wss2.cex.uk.webuy.io/v3/boxes/{product_id}/detail"
        
def get_product(product_id):
    return requests.get(get_product_url(product_id), timeout=5).json()["response"]["data"]["boxDetails"][0]

def get_products_page(categories, page):
	return requests.get(url=get_formatted_url(categories,page), timeout=5).json()

def get_formatted_url(categories, page):
	return f"https://wss2.cex.uk.webuy.io/v3/boxes?&categoryIds=[{','.join(map(str, categories))}]&firstRecord={page}&count=50&inStockOnline=1&sortBy=relevance&sortOrder=desc"

def get_total_records(categories):
	first_page = get_products_page(categories, 1)
	return first_page["response"]["data"]["totalRecords"]

def get_number_of_pages(categories):
	return get_total_records(categories)//50 + 1

def get_products(categories, in_stock_products=None):
	products_json = []
	num_pages = get_number_of_pages(categories)
	for i in range(1, num_pages):
		json_page = get_products_page(categories, i*50+1)
		products_json.extend(json_page["response"]["data"]["boxes"])
	return products_json


