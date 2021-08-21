import socketserver, json
from http.server import BaseHTTPRequestHandler
from urllib import parse
from update import update
from publish import publish
import urllib

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parseRes = urllib.parse.urlparse(self.path)
            if parseRes.path == '/publish':
                if publish() != 0:
                    raise Exception('publish error!')
        except:
            self.send_response(500)
            self.send_header("Content-Type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(bytes("internal error!", "utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(bytes('done', "utf-8"))
    def do_POST(self):
        try:
            subscribe_list = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
            subscribe_list = subscribe_list.split('$')
        except:
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(bytes("parameters error!", "utf-8"))
        else:
            try:
                value = update(subscribe_list)
            except:
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(bytes("update error!", "utf-8"))
            else:
                if type(value).__name__ == 'str':
                    self.send_response(500)
                    self.send_header("Content-Type", "text/html; charset=UTF-8")
                    self.end_headers()
                    self.wfile.write(bytes(value, "utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(value), "utf-8"))
httpd = socketserver.TCPServer(("", 11459), MyHandler)
httpd.serve_forever()
