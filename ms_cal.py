import msal
import os
import requests

CLIENT_ID = os.getenv('MS_CLIENT_ID')
TENANT_ID = os.getenv('MS_TENANT_ID')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["Calendars.ReadWrite"]

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

flow = app.initiate_device_flow(scopes=SCOPE)
if "user_code" not in flow:
    raise Exception("Failed to create device flow")

print(flow["message"])

result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
    print("Signed in as:", result["id_token_claims"]["preferred_username"])

    access_token = result["access_token"]
    # Define event details
    event = {
        "subject": "Python Event Demo",
        "body": {
            "contentType": "HTML",
            "content": "This is a test event created from a Python script."
        },
        "start": {
            "dateTime": "2025-05-23T14:00:00",
            "timeZone": "Pacific Standard Time"
        },
        "end": {
            "dateTime": "2025-05-23T15:00:00",
            "timeZone": "Pacific Standard Time"
        },
        "location": {
            "displayName": "Online"
        }
    }

    endpoint = 'https://graph.microsoft.com/v1.0/me/events'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(endpoint, headers=headers, json=event)

    if response.status_code == 201:
        print("Event created successfully!")
    else:
        print(f"Error creating event: {response.status_code} - {response.text}")

else:
    print("Error:", result.get("error"))
    print(result.get("error_description"))
