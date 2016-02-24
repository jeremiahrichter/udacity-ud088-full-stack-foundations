import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

from jinja2 import Environment, PackageLoader

from database_setup import DBSession, Restaurant

jinja2_env = Environment(loader=PackageLoader('jinja2_templates', 'templates'))


class WebServerHandler(BaseHTTPRequestHandler):
    def get_template(self, template_name):
        t = jinja2_env.get_template(template_name)
        return t

    def render_str(self, template_name, **kwargs):
        t = self.get_template(template_name)
        return t.render(**kwargs)

    def render_page(self, template, **kwargs):
        page_str = self.render_str(template, **kwargs)
        self.wfile.write(page_str)

    def get_hello(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ''
        output += '<html><body>Hello!'
        output += '<form method="POST" enctype="mutipart/form-data" action="/hello"' \
                  '><h2>What would you like me to say?</h2><input name="message" type="text"' \
                  '><input type="submit" value="Submit"></form>'
        output += '</body></html>'
        self.wfile.write(output)
        print(output)

    def get_hola(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ''
        output += '<html><body>&#161Hola!' \
                  '<a href="hello"> Back to Hello </a>'
        output += '<form method="POST" enctype="mutipart/form-data" action="/hello"' \
                  '><h2>What would you like me to say?</h2><input name="message" type="text"' \
                  '><input type="submit" value="Submit"></form>'
        output += '</body></html>'
        self.wfile.write(output)
        print(output)

    def post_hello(self):
        try:
            self.send_response(301)
            self.end_headers()
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            print(form)
            message_content = form.getvalue('message')

            output = ''
            output += '<html><body>'
            output += '<h1>{}</h1>'.format(message_content)
            output += '<form method="POST" action="/hello"' \
                      '><h2>What would you like me to say?</h2><input name="message" type="text"' \
                      '><input type="submit" value="Submit"></form>'
            output += '</body></html>'
            self.wfile.write(output)
            print(output)
        except Exception as e:
            print('An error occurred: {}'.format(e))

    def get_restaurants(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        session = DBSession()
        restaurants = session.query(Restaurant).all()
        self.render_page('restaurants.html', restaurants=restaurants)

    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.get_hello()
            elif self.path.endswith('/hola'):
                self.get_hola()
            elif self.path.endswith('/restaurants'):
                self.get_restaurants()
            elif self.path.endswith('.css'):
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(f.read())
        except IOError:
            self.send_error(404, 'File not found: {}'.format(self.path))

    def do_POST(self):
        if self.path.endswith('/hello') or self.path.endswith('/hola'):
            self.post_hello()


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print('Web server running on port {}'.format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C entered, stopping web server...')
        server.socket.close()


if __name__ == '__main__':
    main()
