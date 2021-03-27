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
    parsed_path = path.split('&')
    question_mark = parsed_path[0].find("?")
    parsed_path[0] = parsed_path[0][question_mark+1::]
    keys = []
    vals = []
    for i in range(len(parsed_path)):
        parsed_path[i] = parsed_path[i].split("=")
        keys.append(parsed_path[i][0])
        vals.append(parsed_path[i][1])
    return dict(zip(keys, vals))



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
        
        if self.path == '/cancel':
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

        if '/action?' in self.path:
            #handle request from scanner
            #request pattenr: action?locati on_id=1&client_id=1&direction=out
            value_key = parse_path_with_args(self.path)
            location_id = value_key["location_id"]
            customer_id = value_key["customer_id"]
            direction = value_key["direction"]
            location = database.get_location(location_id)
            if direction == "in":
                database.get_location(location_id).went_inside(customer_id)
            if direction == "out":
                pass
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
                data = open(self.path[1::]).read()
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
    
    test_locations('Biedronka', [50.0934188, 20.0223255], '')
    test_locations('Biedronka', [50.024036949999996, 20.90635294440421], '')
    test_locations('Biedronka', [50.0079917, 19.9588235], '')
    test_locations('Biedronka', [50.06531735, 20.01617271773779], '')
    test_locations('Biedronka', [50.08660945, 20.0268166642], '')
    test_locations('Biedronka', [50.0842167, 19.924614087677945], '')
    test_locations('Biedronka', [50.0732406, 20.0250832], '')
    test_locations('Biedronka', [50.00630315, 20.019586802444557], '')
    test_locations('Biedronka', [50.078535, 19.8920637], '')
    test_locations('Biedronka', [50.012972250000004, 20.950265216025514], '')

    test_locations('Kaufland', [50.0841107, 19.9362424], '')
    test_locations('Kaufland', [50.02981145, 19.911305415038086], '')
    test_locations('Kaufland', [50.01366645, 19.99631726004617], '')
    test_locations('Kaufland', [50.090278549999994, 20.006228395294286], '')
    test_locations('Kaufland', [50.0146524, 20.02249712916703], '')
    test_locations('Kaufland', [50.0899052, 20.00552454410871], '')
    test_locations('Kaufland', [50.084055649999996, 19.935317076583182], '')
   
    test_locations('Carrefour', [50.0772892, 20.015808], '')
    test_locations('Carrefour', [50.0651897, 19.9845491], '')
    test_locations('Carrefour', [50.06875235, 19.94610034475403], '')
    test_locations('Carrefour', [50.0177032, 19.8934979], '')
    test_locations('Carrefour', [50.0141425, 19.9326706], '')
    test_locations('Carrefour', [50.0111953, 19.96337369866795], '')
    test_locations('Carrefour', [50.0051071, 19.9498077], '')
    test_locations('Carrefour', [50.0150077, 20.0209442], '')
    test_locations('Carrefour', [50.074108, 20.0149843], '')
    test_locations('Carrefour', [50.0768138, 20.01819609740246], '')

    #https://www.openstreetmap.org/geocoder/search_osm_nominatim?query=kaufland+Kraków
    #https://www.openstreetmap.org/search?query=Lewiatan Kraków
   


    


    

  

    httpd = HTTPServer(('localhost', 8080), Serv)
    print("Running server on localhost:8080")
    httpd.serve_forever()
