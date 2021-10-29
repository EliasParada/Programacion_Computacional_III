import datetime

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

def daybetween(date1, date2):
    """
    Returns the number of days between two dates.
    """
    return (date2 - date1).days

def yearbetween(date1, date2):
    """
    Returns the number of years between two dates.
    """
    return (date2.year - date1.year)

date1 = input("Enter the first date (YYYY-MM-DD): ")
date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
date2 = input("Enter the second date (YYYY-MM-DD): ")
date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")

print("The number of days between the two dates is:", daybetween(date1, date2))
print("The number of years between the two dates is:", yearbetween(date1, date2))
print("The number of months between the two dates is:", yearbetween(date1, date2) * 12 + daybetween(date1, date2) // 30)

class basicServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello World</h1></body></html>")

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)