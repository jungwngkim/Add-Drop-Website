import os

# Global variables
# Inserted in global state before request

# Check if server is open to student
server_is_open = False

# student list & current student
waiting_list = []
current_index = 0

priority_list = []

# get environment variable for password
password = [os.environ.get('APP_PASSWORD_1'), os.environ.get('APP_PASSWORD_2')]
google_password = os.environ.get('GOOGLE_PASSWORD')
google_id = os.environ.get('GOOGLE_ID')

print(password)

# 2 user
session = [None, None]
session_key = 'session'

# student id set
register_id_set = set()
