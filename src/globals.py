import os

# Global variables
# Inserted in global state before request

# Check if server is open to student
server_is_open = False

# student list & current student
waiting_list = []
current_index = 0

# get environment variable for password
password = os.environ.get('APP_PASSWORD')
google_password = os.environ.get('GOOGLE_PASSWORD')
google_id = os.environ.get('GOOGLE_ID')

session = None
session_key = 'session'