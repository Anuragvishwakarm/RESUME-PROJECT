import requests
import json

URL = "http://127.0.0.1:8000/Personal/"

def get_data(id=None):
    # Prepare the data as a JSON payload
    data = {}
    if id is not None:
        data = {'id': id}
    
    # Convert data to JSON
    json_data = json.dumps(data)
    
    # Send POST request with JSON data in the body
    response = requests.get(url=URL, data=json_data, headers={'Content-Type': 'application/json'})
    
    try:
        # Parse the response data (JSON)
        data = response.json()
        print(data)
    except json.JSONDecodeError:
        print("Error decoding the response. Make sure the server is running and returning valid JSON.")

# Get student data by ID (change the ID as necessary)
# get_data()



# import requests
# import json

# # Set the URL to your Django API endpoint
# URL = "http://127.0.0.1:8000/studentapi/"

def post_data():
    # Prepare the data to send in the POST request
    data = {
    'name' :'Anurag',
    'email' :'anuragkumar123@gmail.com',
    'mobile': '457689899',
    'address':'delhi' ,
    'linkedin_url' :'',
    'github_link' :'' 
    }
    
    # Convert the Python dictionary to JSON format
    json_data = json.dumps(data)
    
    # Send POST request with JSON data in the request body
    response = requests.post(url=URL, data=json_data, headers={'Content-Type': 'application/json'})
    
    try:
        # Parse the response data (JSON) if the response is valid
        data = response.json()
        print(data)
    except json.JSONDecodeError:
        print("Error decoding the response. Make sure the server is running and returning valid JSON.")

# Call the function to send the POST request with the student data
post_data()
