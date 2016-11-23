from src import app
from flask import jsonify, make_response
import models, datetime

def getProductEntries(product): 
    entry_list = []
    if product:
        for e in product.entries:
            entry_list.append({"food_id": e.food.id, "food_name" : e.food.name, 
                "location_id" : e.source.id, "location_name" : e.source.name,
                "price" : e.price, "date" : e.date.isoformat()})
    
    return entry_list

@app.route("/api/product")
def all_products():
    product_info = {} #setup the return object
    products = models.Product.query.all() #get all products
    for p in products: 
        entry_list = None
        entry_list = getProductEntries(p)
        
        #don't store/return an empty object
        if entry_list: 
            product_info[p.name] = [entry_list] 
    
    #the std lib's jsonify method will not JSONIFY a decimal.DECIMAL object 
    #the package 'simplejson' however DOES infact jsonify a decimal 
    #if you downlaod the 'simplejson' package, Flask will auto use it 
    return jsonify(product_info)

@app.route("/api/product/<product_id>")
def product(product_id): 
    product = models.Product.query.filter_by(id=product_id).first()
    entries = getProductEntries(product)
    if entries: 
        return jsonify(entries)
    
    return '', 204

def scraperToDB(scraper_JSON):
	obj = json.loads(scraper_JSON)
	foundProd = list()

	#find products in JSON
	for loc in obj:
		for prod in obj[loc]:
			if (prod not in foundProd):
				foundProd.append(prod)

	#new JSON builder
	jStr = "{"
	multiple = False #for multiple locations under one product
	t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	for p in foundProd:
		if (jStr <> "{"):#add ','
			jStr += ','
		multiple = False
		jStr += '"' + p + '": [['
		for l in obj:
			if (p in obj[l]): #add it to the JSON
				if (multiple):
					jStr += ","
				pID = models.Product.query.filter_by(name=p).first()
				lID = models.Location.query.filter_by(name=l).first()
				jStr += '{'
				jStr += '"date": "' + t + '",'
				jStr += '"food_id": ' +  str(pID)  + ','
				jStr += '"food_name": "' + p + '",'
				jStr += '"location_id": ' + str(lID) + ','
				jStr += '"location_name": "' + l + '",'
				jStr += '"price": ' + str(obj[l][p])
				jStr += '}'
				multiple = True
		jStr += ']]'

	jStr += '}'
	return jStr


