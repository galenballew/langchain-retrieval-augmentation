"""debugserver.py
Debug server.
You do not need to edit this file.
"""
import api
import gzip, json, base64
from http.server import BaseHTTPRequestHandler, HTTPServer

DEBUG_SERVER_PORT = 8000 # Use env variables instead of changing this value
FOUR_OH_FOUR = '''<!doctype html><html><head>
    <title>404 Not Found</title>
  </head>
  <body>
    <h1>404 Not found</h1>
    <p>The resource specified was not found.</p>
  </body>
</html>'''

FILES = json.loads(gzip.decompress(base64.b64decode('H4sIAC4meGQC/8VXe2/bNhD/KlzQQTJmSU6HDoVjd8PaAOvQF5Dsj6EuClo8S4xpUiBpO0aQ774jqafjrssGrA5ik7wH7/G7I3l3lp1NydlCzr5jKreHCkhpN+LFzH8vJCGzEijzIxxvwFKSl1QbsPPF2daukueLswFV0g0gacdhXyltF2ckV9KCdPx7zmw5Z7DjOSR+MiZccsupSExOBczPO22WWwEvXpbULpUlr2C5LWZZWKw5BJdrokGgZmMPAkwJ4DYsNaxwrbS2MtMsy5lMbwwDwXc6lWAzWW2ypVLWWE2rX56lk3SSLNH2HzPGjc1yYzpyuuEyxRVU+3CngSH1rpln+KqIyTWvLDE671lagbVU3pi04LbcLlOuMrbKb4z7RhdQocsQCli4tdkN3dGgBtXOsjA8qT9bUgOPUTDL2qzPlood2gxTLkkuqDGow+UV56Bbrxxazlv6xibPkOQyiPrOOx7Gdy2TVvue+BExV2JArMmcORqqFapw+Gq4cSXpGzXDfO76ugfzo9ljjErOJ8d2cVltbbBsa0AnLsA921ZKb7xtWgnSnySiGGYFZ5WgOZRKMNC4eO2K0lFICRqGdh07eGznU8KSQnN2bO1ya62SwVwDknUmBErP8qWVBP+TSvMN1Qc/FoX/WQqVr1H1FWqYZUHyH4V7ljkg1Uir8YUQaVrO2Zi0kA3dCYNlLHn7/tXl1fWfby6vyJzcOc7IxTqaksjnfmMKklPNyLJozV0JhRQ00IcwEbwobTT2sthWTop6nlrQWKptEGVUr2tJ0Fqd3pZRWYB+KBz2Xcj7i4XcUU0+owdY1PXsCc5WW5lbjkmJYUTusHPYrZYEm/J2g80zLcBeCnDDXw+vGfJckPuFXMhWzPXRKzAGx/EoRKfWsQKbl3GU0Ypn3qTPJvBF48CHHmHrLhVzLn14f3Ud3MRl1wVAG1y/a/IYvQztPHG4dAK0qgTPqTMiuzGoNXDeNzpcfh3f3b2n3I9SW4KMO381mGrUbFDb7NZSpy0eXZyWYtTSVoqvSFxnBQNBBjRCbIkFTSTsyaVj8aKp5w7KUT0BYaCTaKKPjB8jq9Ygo08NazAHZ8P4b+ga3mJcaQF/8NglfUw2ioG3w8m4RDu4vkW4zMnnOMJ66DKAgfIV9w6PT4xW7ESdKz3M/9yVVrf60TF+ItOO9jhAj5pskY9fManV63ubV5743A40oLgjjz7hn4/YkziqW3U0ShErWIovSy5YXMfiBBceREqIa1VhnE4QfgPnz0UP4bWqBzlxra3OSeyziCkJ0xodDjf1SmqxY8SjVIAsbEnm8zmZHKPyg1Ybjm0J0anEDhpsuq9h+mud47pBtT62RwM6s6NiC+hhFHlqv0od+pVk/2t9/n71/l2KVx4uC746xJ2+AP8pCQFsl2sXkVCParWjb1TkwwR0JT5u2nVT6/+mH5xQHnJkXI7dQTL6++7AAEOrDk2D9rH8cpdG2H6THn2MgWHu/1tq64jsuWRqn1LGLndo4Ru8cAPe1uIIu5MDfKe2KdH+uXa8dT+OvsBcxbs+80B9jv6vT+l3nxN94lSxtuhoBkdMD3ddwwG9lYN9obexgzS+FVyvdw0nusS0IVI7hkfbVkOwZ+QXI74EvIjCVn4p8u5zErfDMCAgEFmI3VMu4ptO2zh6jUkkK8oFMLQH22tEfiDQyLtqGbUXv/b9FK5+aXuc3YU+extejlPyfPL9RVjSBcfbqML752ZKzifVrV9XO9B46O2T2ymhW6v8Yi6A6ilB5jIUaTo81vwm+5JbSEyF1/ApqTS+VfEl2GdvXxmBv/Qn0pT8NGn2rjDcWEVT8rRZObLy6QMrD1MSzrewEUbj/i8f/KAMng8AAA==')).decode('utf-8'))
class DebugServer(BaseHTTPRequestHandler):
  def _sniff_type(self):
    if self.path.endswith('.js'):
      return 'text/javascript'
    elif self.path.endswith('.css'):
      return 'text/css'
    elif self.path.endswith('.html') or \
      self.path.endswith('.htm') or \
      self.path.endswith('/'):
      return 'text/html'
    else:
      return 'application/octet-stream'

  def do_GET(self):
    if self.path == '/index.html' or self.path == '/index.htm':
      self.send_response(301)
      self.send_header('location', '/')
      self.end_headers()
    elif self.path in FILES:
      self.send_response(200)
      self.send_header('content-type', self._sniff_type())
      self.end_headers()
      self.wfile.write(bytes(FILES[self.path], "utf-8"))
    else:
      self.send_response(404)
      self.send_header('content-type', 'text/html')
      self.end_headers()
      self.wfile.write(bytes(FOUR_OH_FOUR, 'utf-8'))

  def do_POST(self):
    if self.path.startswith('/api/'):
      code, resp = 200, None
      try:
        # Get the body
        body_len = int(self.headers.get('Content-Length'))
        body = json.loads(self.rfile.read(body_len))
        if self.path.endswith('/start_session'):
          resp = { 'token': api.start_session() }
        elif self.path.endswith('/end_session'):
          api.end_session(body['token'])
          resp = { 'success': True }
        elif self.path.endswith('/respond'):
          resp = { 'response': api.respond(body['token'], body['message']) }
      except Exception as e:
        code = 500
        print(e)
        resp = { 'error': str(e) }
      self.send_response(code)
      self.send_header("content-type", "application/json")
      self.end_headers()
      self.wfile.write(bytes(json.dumps(resp), 'utf-8'))
    else:
      self.send_response(404)
      self.send_header('content-type', 'text/html')
      self.end_headers()
      self.wfile.write(bytes(FOUR_OH_FOUR, 'utf-8'))

if __name__ == '__main__':
  import os
  import socketserver
  port = int(os.environ['PORT']) if 'PORT' in os.environ else DEBUG_SERVER_PORT

  socketserver.TCPServer.allow_reuse_address = True
  with socketserver.TCPServer(("", port), DebugServer) as httpd:
    print(f'Serving HTTP debug console on port {port}')
    httpd.serve_forever()
