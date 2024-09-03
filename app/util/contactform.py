import requests
import json

# Your Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/1066880915101450240/-F7g5n0Kldsun8ARKw1cOvA05GlCXXFSJ82DqkvRYfziBDH7rQF1xJu0bMj1_9QE2CrA'



# Define the embed message
def send_form(name,email,content):

    embed = {
        "title": "Contact form submitted",
        "url": "https://supertips.app/",
        "color": 15258703,  # Hex color code
        "fields": [
            {
                "name": "Name",
                "value": name,
                "inline": False
            },
            {
                "name": "E-mail address",
                "value": email,
                "inline": True
            },
            {
                "name": "Content",
                "value": content,
                "inline": True
            }
        ]
    }

    # Create the payload with the embed
    data = {
        "content": "Contact form alert!",
        "embeds": [embed]
    }

    # Send the POST request to the webhook URL
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
