import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from views import get_single_entry, get_all_entries, get_all_moods, get_single_mood, delete_entry

class HandleRequests(BaseHTTPRequestHandler): 
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path): 

        path_params = path.split("/")
        resource = path_params[1]

        pk = None
        try: 
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)
    
    def do_GET(self):
        """Handles GET requests to the server """
        response = {}
        self._set_headers(200)
        (resource, id) = self.parse_url(self.path)

        if resource == "entries": 
            if id is not None: 
                response = get_single_entry(id)
            else: 
                response = get_all_entries()

        if resource == "moods":
            if id is not None: 
                response = get_single_mood(id)
            else: 
                response = get_all_moods()

        self.wfile.write(json.dumps(response).encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "entries": 
            delete_entry(id)
        self.wfile.write("".encode())
            



# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()