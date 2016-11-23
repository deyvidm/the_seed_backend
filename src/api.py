from src import app
from flask import jsonify
import models, datetime

@app.route("/api/product")
def index():
    
    product_info = {} #setup the return object
    products = models.Product.query.all() #get all products
    for p in products: 
        entry_list = [] #setup the collection of entries per food
        
        for e in p.entries:
            entry_list.append({"food_id": e.food.id, "food_name" : e.food.name, 
                "location_id" : e.source.id, "location_name" : e.source.name,
                "price" : e.price, "date" : e.date.isoformat()})
        
        #just in case there are no entries for this food
        #don't return an empty object
        if entry_list: 
            product_info[p.name] = [entry_list] 
    
    #the std lib's jsonify method will not JSONIFY a decimal.DECIMAL object 
    #the package 'simplejson' however DOES infact jsonify a decimal 
    #if you downlaod the 'simplejson' package, Flask will auto use it 
    return jsonify(product_info)
