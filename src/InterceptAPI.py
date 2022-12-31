import cgi
from http.server import BaseHTTPRequestHandler
import io


class Intercept(BaseHTTPRequestHandler):

    def do_GET(self):
        # Begin the response
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Nice Get Request')

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        print(post_body.decode(encoding='UTF-8'))
        
        # Begin the response
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Nice Post Request')


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 4205), Intercept)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()