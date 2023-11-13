#!/usr/bin/env python3

'''
app.py is the starting point of the application; to run the app, in the console, you run "python app.py"
'''
import os
import sys

from app import app

# Builds the server configuration
if os.getenv('IP'):
  IP    = os.getenv('IP')
else:
  IP    = '0.0.0.0'

if os.getenv('PORT'):
  PORT  = int(os.getenv('PORT'))
else:
  PORT  = 8080

if __name__ == "__main__":
    # Print statements go to your log file in production; to your console while developing
    print ("Environment:", os.getenv('APP_ENV', 'production'))
    print ("Running server at http://{0}:{1}/".format(IP, PORT))
    app.run(host = IP, port = PORT, debug = True, threaded = True)

# The next logical place to look is the app/__init__.py file...
