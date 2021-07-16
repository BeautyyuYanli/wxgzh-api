import socketserver, json
from http.server import BaseHTTPRequestHandler
from update import update
from urllib.parse import unquote

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            subscribe_list = self.path.split('query=')[1]
            subscribe_list = unquote(subscribe_list)
            subscribe_list = subscribe_list.split('$')
        except:
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=UTF-8")
            self.end_headers()
            self.wfile.write(bytes("parameters error!", "utf-8"))
        else:
            # value = update(subscribe_list)
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
