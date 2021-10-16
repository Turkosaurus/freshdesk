import os
import json
import requests

print("--- FRESHDESK ---")

## Freshdesk credentials
# API
api_key = os.environ.get('API_KEY')
if not api_key:
    print("Error: api_key not found.")
else:
    print("API key found.")

# Password
password = os.environ.get('FD_PASSWORD')
if not password:
    print("Error: password not found.")
else:
    print("Password found.")

# Domain
domain = 'restaurant365'
print(f"Domain set to '{domain}'.")
print("Requesting data...")


def get_tickets():

    r = requests.get("https://"+ domain +".freshdesk.com/api/v2/tickets", auth = (api_key, password))

    if r.status_code == 200:
        print("Request processed successfully, the response is given below")
        return r.content

    else:
        print("Failed to read tickets, errors are displayed below")
        response = json.loads(r.content)
        print(response["errors"])

        print(f"x-request-id : " + {r.headers['x-request-id']})
        print(f"Status Code : " + {str(r.status_code)})

        return 'error'


# Load and count ticket data
data = get_tickets()
tickets = json.loads(data)
total = 0
for ticket in tickets:
    total += 1
print(f"Loaded data for {total} tickets.")
if data == 'error':
    print('Failed to get tickets.')


# Main function
active = True
while active == True:
    request = input("Type 'exit', 'list', or enter ticket #:")

    if request == 'list':
        print(f"Listing {total} tickets...")
        for ticket in tickets:
            print(f"{ticket['id']} {ticket['subject']}")

    # Interrupt
    elif request == 'exit':
        print("Exiting...")
        break

    else:
        print(f"Retrieving data for ticket: {request}")
        result = None

        for ticket in tickets:
            if int(ticket['id']) == int(request):
                print(f"matched {ticket['id']} to {request}")
                result = ticket

        if result is None:
            print(f"Ticket #{request} not found.")

        else:
            print(f"id: {result['id']}")
            print(f"subject: {result['subject']}")
            print(f"status: {result['status']}")
            print(f"Product: {result['custom_fields']['cf_product_service']}")

            print(result['custom_fields'])

            # for key, value in result.items():
            #     print(f"{key}: {value}")
