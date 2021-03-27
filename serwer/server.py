from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json, mimetypes, threading, time
from db import DB
from hashlib import sha256 
from jinja2 import Template, Environment, FileSystemLoader
from urllib.parse import unquote
from db import Customer
from http.cookies import SimpleCookie

html_path = '/html'

database = DB()

env = Environment(loader=FileSystemLoader('html'))

def add_reservation(dane):
    global database
    dane = unquote(dane)
    print(dane)
    parsed_string = dane.replace('+', ' ').split('=')
    # name = parsed_string[1].split('&')[0].strip()
    location_id = parsed_string[1].split('&')[0].strip()
    customer_id = parsed_string[2].strip()
    print(location_id, customer_id)
    customer = Customer(customer_id)
    if database.get_location(location_id).add_to_queue(customer):
        return True
    print("Blad podczas dodawania")
    return False

def create_location(dane):
    global database
    dane = unquote(dane)
    print(dane)
    parsed_string = dane.replace('+', ' ').split('=')
    name = parsed_string[1].split('&')[0].strip()
    address = parsed_string[2].split('&')[0].strip()
    size = parsed_string[3].strip()
    hash_data = f'{name}{address}{size}'
    locationid = sha256( bytes(hash_data, encoding='utf-8') ).hexdigest()
    print(name, address, size, locationid)
    if database.add_location(locationid, name, address, int(size) ):
        return True
    return False

class Serv(BaseHTTPRequestHandler):
    global database
    
    def do_POST(self):
        print("Zapytanie POST")
        print(self.path)
        
        if self.path == '/create':
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length) 
            #Parse POST data, and send response
            if create_location(post_data.decode('utf-8')):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('ok', "utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('ok', "utf-8"))

        elif self.path == '/reserve':
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length) 
            #Parse POST data, and send response
            if add_reservation(post_data.decode('utf-8')):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('ok', "utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('ok', "utf-8"))
        
        

    def do_GET(self):
        if self.path == '/':
            template = env.get_template('index.html')
            output_from_parsed_template = template.render(locations=database.get_all())

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output_from_parsed_template, "utf-8"))
            return

        if self.path == '/create':
            template = env.get_template('create.html')
            output_from_parsed_template = template.render(locations=database.get_all())
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output_from_parsed_template, "utf-8"))
            return


        if self.path == '/register':
            template = env.get_template('register.html')
            output_from_parsed_template = template.render(locations=database.get_all())
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output_from_parsed_template, "utf-8"))
            return

        if self.path == '/status':
            cookie = self.headers.get('Cookie')
            status = database.queue_index(cookie)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(status), "utf-8"))
            return
        # # Clear the database before new game/round
        # elif self.path.startswith('/reset'):
        #     data = get_db()
        #     data.clear()
        #     self.send_response(200)
        #     self.send_header("Content-type", "text/html")
        #     self.end_headers()
        #     self.wfile.write(bytes("Database cleared", "utf-8"))
        #     return

        else:
            if self.path[1::].endswith('.jpg'):
                print("Opening here")
                data = open(self.path[1::], 'rb').read()
                mimetype = 'image/jpeg'
                self.send_response(200)            
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(data)
                return
            else:
                data = open(self.path[1::]).read()
                mimetype, _ = mimetypes.guess_type(self.path[1::])
            self.send_response(200)            
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(bytes(data, "utf-8"))
            return

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8080), Serv)
    print("Running server on localhost:8080")
    httpd.serve_forever()
