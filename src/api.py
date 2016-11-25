from src import app, db
from flask import jsonify, abort, make_response, g, request, url_for
import models, datetime
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
import subprocess
# extensions
auth = HTTPBasicAuth()

@app.route("/api/scrape", methods=['POST'])
@cross_origin()
@auth.login_required
def scrape():
    if (not subprocess.call(["python", "turtleScrapes/WebsiteScraper.py"])):
        if (not subprocess.call(["./fromScraper.py", "turtleScrapes/scraped.json"])):
            return 'success'
    return 'ah fuck, something went wrong', 500


def getProductEntries(product): 
    entry_list = []
    if product:
        for e in product.entries:
            entry_list.append({"food_id": e.food.id, "food_name" : e.food.name, 
                "location_id" : e.source.id, "location_name" : e.source.name,
                "price" : e.price, "date" : e.date.isoformat()})
    
    return entry_list

@app.route("/api/product")
@cross_origin()
def all_products():
    product_info = {} #setup the return object
    products = models.Product.query.all() #get all products
    for p in products: 
        entry_list = None
        entry_list = getProductEntries(p)
        
        #don't store/return an empty object
        if entry_list: 
            product_info[p.name] = entry_list
    
    #the std lib's jsonify method will not JSONIFY a decimal.DECIMAL object 
    #the package 'simplejson' however DOES infact jsonify a decimal 
    #if you downlaod the 'simplejson' package, Flask will auto use it 
    return jsonify(product_info)

@app.route("/api/product/<product_id>")
@cross_origin()
def product(product_id): 
    product = models.Product.query.filter_by(id=product_id).first()
    entries = getProductEntries(product)
    if entries: 
        return jsonify(entries)
    
    return '', 204

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = models.User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/users', methods=['POST'])
@cross_origin()
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400) # missing arguments
	if models.User.query.filter_by(username=username).first() is not None:
		abort(400) # existing user
	user = models.User(username=username)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return (jsonify({'username': user.username}), 201,
		    {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
@cross_origin()
def get_user(id):
	user = models.User.query.get(id)
	if not user:
		abort(400)
	return jsonify({'username': user.username})

@app.route('/api/token')
@cross_origin()
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token(2400)
	return jsonify({'token': token.decode('ascii'), 'duration': 2400})

@app.route('/api/resource')
@cross_origin()
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s!' % g.user.username})
