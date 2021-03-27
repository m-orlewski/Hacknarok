from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json, mimetypes, threading, time, random, string
from db import DB
from hashlib import sha256 
from jinja2 import Template, Environment, FileSystemLoader
from urllib.parse import unquote
from http.cookies import SimpleCookie

html_path = '/html'

database = DB()

env = Environment(loader=FileSystemLoader('html'))

def add_reservation(dane):
    global database
    dane = unquote(dane)
    parsed_string = dane.replace('+', ' ').split('=')
    location_id = parsed_string[1].split('&')[0].strip()
    customer_id = parsed_string[2].strip()
    if database.get_location(location_id).add_to_queue(customer_id):
        return True
    print("Blad podczas dodawania")
    return False

def create_location(dane):
    global database
    dane = unquote(dane)
    parsed_string = dane.replace('+', ' ').split('=')
    name = parsed_string[1].split('&')[0].strip()
    address = parsed_string[2].split('&')[0].strip()
    coords = parsed_string[3].split('&')[0].strip()
    size = parsed_string[4].strip()
    hash_data = f'{name}{address}{coords}{size}'
    locationid = sha256( bytes(hash_data, encoding='utf-8') ).hexdigest()
    if database.add_location(locationid, name, address, coords, int(size) ):
        return True
    return False


def parse_path_with_args(path):
    path = unquote(path)
    path = path[path.find('?')+1:].split('&')
    data = {}
    for el in path:
        data[ el[:el.find('=')] ] = el[el.find('=')+1:]
    return data



class Serv(BaseHTTPRequestHandler):
    global database
    
    def do_POST(self):
        print("Zapytanie POST")        
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
        print(self.path)
        if self.path == '/':
            template = env.get_template('index.html')
            output_from_parsed_template = template.render(locations=database.get_all())

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output_from_parsed_template, "utf-8"))
            return

        elif self.path == '/create':
            template = env.get_template('create.html')
            output_from_parsed_template = template.render(locations=database.get_all())
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output_from_parsed_template, "utf-8"))
            return


        elif self.path == '/register':
            template = env.get_template('register.html')
            output_from_parsed_template = template.render(locations=database.get_all())
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output_from_parsed_template, "utf-8"))
            return

        elif self.path == '/status':
            cookie = self.headers.get('Cookie')
            status = database.queue_index(cookie)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(status), "utf-8"))
            return
        
        elif self.path == '/cancel':
            print("CANCELING")
            cookie = self.headers.get('Cookie')
            status = database.queue_index(cookie)
            if database.get_location(status[0]).remove_from_queue(cookie):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('ok', "utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('err', "utf-8"))

        elif '/action?' in self.path:
            #handle request from scanner
            #request pattenr: action?locati on_id=1&client_id=1&direction=out
            value_key = parse_path_with_args(self.path)
            customer_id = value_key["cusomterID"]
            location_id = value_key["locationID"]
            print(location_id, customer_id)
            location = database.get_location(location_id)
            data = location.switch_user(customer_id)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes('ok', "utf-8"))
            return

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
                data = open(self.path[1::], encoding='utf8').read()
                mimetype, _ = mimetypes.guess_type(self.path[1::])
            self.send_response(200)            
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(bytes(data, "utf-8"))
            return


def test_locations(name, coords, address):
    global database
    size = random.randint(20, 1000)
    hash_data = f'{name}{address}{coords}{size}'
    locationid = sha256( bytes(hash_data, encoding='utf-8') ).hexdigest()
    database.add_location(locationid, name, address, coords, int(size) )



if __name__ == "__main__":
    
    test_locations('Biedronka', [50.0934188, 20.0223255], 'Generała Leopolda Okulickiego')
    test_locations('Biedronka2', [50.0732406, 20.0250832], 'Generała Leopolda Okulickiego')


    httpd = HTTPServer(('localhost', 8080), Serv)
    print("Running server on localhost:8080")
    httpd.serve_forever()
