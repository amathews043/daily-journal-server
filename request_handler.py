import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from views import get_single_entry, get_all_entries, get_all_moods, get_single_mood, delete_entry, create_entry, update_entry
from views import get_entry_by_search
from urllib.parse import urlparse, parse_qs

class HandleRequests(BaseHTTPRequestHandler): 
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path): 
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try: 
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)
    
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_entry = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "entries":
            new_entry = create_entry(post_body)

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_entry).encode())
    
    def do_GET(self):
        """Handles GET requests to the server """
        response = {}
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id ) = parsed

            if resource == "entries": 
                if id is not None: 
                    self._set_headers(200)
                    response = get_single_entry(id)
                    if response is None:
                        self._set_headers(404)
                        response = {
                            "message": f"There is no entry with that id"}
                else: 
                    self._set_headers(200)
                    response = get_all_entries()

            if resource == "moods":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_mood(id)
                else: 
                    self._set_headers(200)
                    response = get_all_moods()
            
        else: 
            (resource, query) = parsed
            self._set_headers(200)

            if query.get('q') and resource == 'entries':
                response = get_entry_by_search(query['q'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self): 
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries": 
            success = update_entry(id, post_body)
        
        if success: 
            self._set_headers(204)
        else: 
            self._set_headers(400)
        
        self.wfile.write("".encode())

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