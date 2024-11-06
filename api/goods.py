from flask import Flask, request
from flask_restful import Resource, Api
import psycopg2
import psycopg2.extras
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    'uiversion': 3,
    'swagger_ui': True,  # Включение Swagger UI
    'url_prefix': '/',  # Изменение URL на '/'
     'swagger_ui_css': '/static/custom.css',
     "static_url_path": "/flasgger_static",
     "swagger_ui": True,
     "specs_route": "/",
}
swagger = Swagger(app,template_file='swagger.yaml')
API_KEY = "dfgkd58345f8i43fd83s9sdv"
isAutorised = False



class Autorisation(Resource):
    def get(self):
        groups_list = []
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
            
            groups_list.append({'isAutorise': "true", 'error': "none"})
            isAutorised = True
            
        else:
            groups_list.append({'isAutorise': "false",'error': "API ключ не корректен, или указан неверно"}) 
            isAutorised = False
        return groups_list
api.add_resource(Autorisation, '/autorisation')

class Category(Resource):
   
    def get(self):
        
        groups_list = []
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
          
            try:
                conn = psycopg2.connect(host='localhost', user='api_dns', password='qwerty', dbname='goods', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute('SELECT * FROM categories ORDER BY category_name ASC')
                for row in cursor:
                    id = row['category_id']
                    name = row['category_name']
                    logo = row['category_logo']
                    groups_list.append({'id': id, 'name': name, 'logo': logo})
                conn.close()
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            groups_list.append({'error': "API ключ не корректен, или указан неверно"}) 
        return groups_list
api.add_resource(Category, '/categories')

class Manufacturers(Resource):
    def get(self):
        groups_list = []
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
            
            try:
                conn = psycopg2.connect(host='localhost', user='api_dns', password='qwerty', dbname='goods', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute('SELECT * FROM public.manufacturers ORDER BY manufacturer_id ASC ')
                for row in cursor:
                    id = row['manufacturer_id']
                    name = row['manufacturer_name']
            
                    groups_list.append({'id': id, 'name': name})
                conn.close()
            except Exception as e:
                print(str(e))
                return str(e)
            
        else:
            groups_list.append({'error': "API ключ не корректен, или указан неверно"}) 
        return groups_list
api.add_resource(Manufacturers, '/manufacturers')

class Customers(Resource):
    def post(self):
        groups_list = []
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
            data = request.json
            try:
                conn = psycopg2.connect(host='localhost', user='api_dns', password='qwerty', dbname='goods', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(f'''INSERT INTO public.customers ("customer_name") VALUES('{data["new_customer_name"]}') ''')
                print (data)
                conn.commit() 
                conn.close()
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            groups_list.append({'error': "API ключ не корректен, или указан неверно"}) 
        return groups_list
        
    def put(self, id):
        groups_list = []
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
            data = request.json
            try:
                conn = psycopg2.connect(host='localhost', user='api_dns', password='qwerty', dbname='goods', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(f'''UPDATE public.customers SET customer_name={data["new_name"]} WHERE customer_id ={id} ''')
                print (data)
                conn.commit() 
                conn.close()
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            groups_list.append({'error': "API ключ не корректен, или указан неверно"}) 
        return groups_list
            
    def delete(self, id):
        groups_list = []
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
            try:
                conn = psycopg2.connect(host='localhost', user='api_dns', password='qwerty', dbname='goods', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(f'''DELETE FROM public.customers  WHERE customer_id={id}''')
                print ("deleted")
                conn.commit() 
                conn.close()
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            groups_list.append({'error': "API ключ не корректен, или указан неверно"}) 
        return groups_list
        
    def get(self,id=None):
        groups_list = []
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
            
            try:
                conn = psycopg2.connect(host='localhost', user='api_dns', password='qwerty', dbname='goods', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                if id is None:
                    cursor.execute(f'SELECT * FROM public.customers')
                    for row in cursor:
                        cid = row['customer_id']
                        name = row['customer_name']
                        groups_list.append({'id': cid, 'name': name})
                else:
                    cursor.execute(f'SELECT * FROM public.customers WHERE customer_id ={str(id)}')
                    for row in cursor:
                        cid = row['customer_id']
                        name = row['customer_name']
                        groups_list.append({'id': cid, 'name': name})
                conn.close()
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            groups_list.append({'error': "API ключ не корректен, или указан неверно"}) 
        return groups_list

api.add_resource(Customers, '/customers','/customers/<int:id>')

class Products(Resource):
    def get(self):
        groups_list = []
        getMid = str(request.args.get('manufacturer_id', default='0'))
        getCid = str(request.args.get('category_id', default='0'))
        getMname = request.args.get('manufacturer_name', default='0')
        getCname = request.args.get('category_name', default='0')
        UserApKey = request.args.get('apikey', default='0')
        if (UserApKey==API_KEY):
            try:
                conn = psycopg2.connect(host='localhost', user='api_dns', password='qwerty', dbname='goods', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                query ='''SELECT product_id, product_name, p.manufacturer_id,p.category_id,category_name,manufacturer_name FROM public.products as p 
                JOIN categories as c on p.category_id=c.category_id 
                JOIN manufacturers as m on p.manufacturer_id=m.manufacturer_id'''
                argum = " WHERE"
                if(getMid !="0"):
                    query =query+argum+" m.manufacturer_id = "+getMid
                    argum= " AND" 
                if(getCid !="0"):
                    query =query+argum+" c.category_id = "+getCid 
                    argum= " AND"         
                if(getMname !="0"):
                    query =query+argum+" m.manufacturer_name LIKE '"+getMname+"'" 
                    argum= " AND"
                if(getCname !="0"):
                    query =query+argum+" c.category_name  LIKE '"+getCname +"'"
                    argum= " AND"
                cursor.execute(query)
                for row in cursor:
                    id = row['product_id']
                    name = row['product_name']
                    mid = row['manufacturer_id']
                    cid = row['category_id']
                    cname = row['category_name']
                    mname = row['manufacturer_name']
                    groups_list.append({'id': id, 'name': name, 'manufacturer_id': mid,"manufacturer_name":mname,"category_id":cid,"category_name":cname})
                conn.close()
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            groups_list.append({'error': "API ключ не корректен, или указан неверно"}) 
        return groups_list
api.add_resource(Products, '/products')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
