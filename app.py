from flask import Flask, jsonify, request

app = Flask(__name__)

from products import products # importa el diccionario  para luego leer, añadir, modificar, borrar
#ten en cuenta que el diccionario esta en otro fichero aparte sino lo importara, 
#no podria tener acceso a el

@app.route("/")
def saludo():
    return("Bienvenido a mi API REST")
# Testing Route
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

# Get Data Routes
#@app.route('/products',methods=['GET']) por defecto es el metodo get por eso NO SE PONE
@app.route('/products')
def getProducts():
    # return jsonify(products)
    #jsonify devuelve una respueta en formato JSON
    return jsonify({'products': products})


@app.route('/products/<string:product_name>')
def getProduct(product_name):
    encontrado=False
    for product in products:
        if product['name'].lower() == product_name.lower():
            productsFound=product
            encontrado=True
        
    
    if encontrado==True:
        return jsonify({'product': productsFound})
    else:
        return jsonify({'message': 'Producto no encontrdo'})

# Create Data Routes
@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        'name': request.json['name'],
        'price': request.json['price'],
        'quantity': request.json['quantity']
    }
    products.append(new_product)
    return jsonify({'mensaje':'Producto agregado correctamente','products': products})

# Update Data Route
@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    for product in products:
        if product['name'] == product_name.lower():
            productsFound=product
    #productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound) > 0):
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            'message': 'Producto Modificado Correctamente',
            'product': productsFound[0]
        })
    return jsonify({'message': 'Producto No encontrado'})

# DELETE Data Route
@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    for product in products:
        if product['name'] == product_name.lower():
            productsFound=product
    #productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            'message': 'Producto Borrado',
            'products': products
        })

if __name__ == '__main__':
    app.run(debug=True, port=4000)
