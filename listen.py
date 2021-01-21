import socketserver, json
from http.server import BaseHTTPRequestHandler
from update import update
from urllib.parse import unquote

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        try:
            subscribe_list = self.path.split('query=')[1]
            subscribe_list = unquote(subscribe_list)
            subscribe_list = subscribe_list.split('$')
        except:
            self.wfile.write(bytes("parameters error!", "utf-8"))
        else:
            try:
                value = update(subscribe_list)
            except:
                self.wfile.write(bytes("update error!", "utf-8"))
            if type(value) == type("faq"):
                self.wfile.write(bytes(value, "utf-8"))
            else:
                self.wfile.write(bytes(json.dumps(value), "utf-8"))
httpd = socketserver.TCPServer(("", 11459), MyHandler)
httpd.serve_forever()
