from http.server import HTTPServer, BaseHTTPRequestHandler
import IPManager

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if(self.path == '/'):
            self.path = '../FrontEnd/index.html'
        if (self.path == '/prediction'):
            self.path = '../FrontEnd/prediction.html'
        if (self.path == '/results'):
            self.path = '../FrontEnd/results.html'
        try:
            file = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file, 'UTF-8'))

def main():
    PORT = 8000
    server = HTTPServer(('', PORT), Server)
    server.serve_forever()
    ipm = IPManager()


if(__name__ == '__main__'):
    main()