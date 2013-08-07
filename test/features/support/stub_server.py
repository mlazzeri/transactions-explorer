from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import re
import threading
import time
import requests

STATUS_RESOURCE = 'http://localhost:8000/high-volume-services/by-transactions-per-year/descending.html'

HTML_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'output'))


def rewrite_request(path):
    new_path = path
    if not re.match(r'.*\..*$', path):
        new_path += '.html'

    return new_path


def wait_until(condition, timeout=15, interval=0.1):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if condition():
            return
        time.sleep(interval)
    raise RuntimeError("timeout")


class HttpStub(BaseHTTPRequestHandler):

    thread = None
    server = None

    def do_GET(self):
        # rewrite requests to point at flat *.html files
        path_to_html = rewrite_request(self.path)
        full_path = HTML_ROOT + path_to_html

        if not os.path.isfile(full_path):
            self.send_response(404)
        
        else:
            with open(full_path, mode='r') as f:
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                self.wfile.write(f.read())

        return

    @classmethod
    def start(cls):
        cls.server = HTTPServer(("", 8000), cls)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()
        wait_until(cls._running)

    @classmethod
    def stop(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    @classmethod
    def _running(cls):
        try:
            return requests.get(STATUS_RESOURCE).status_code == 200
        except:
            return False


if __name__ == "__main__":
    HttpStub.start()
