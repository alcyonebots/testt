import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Replace these with your actual API ID and hash
API_ID = 29872536  # Replace with your API ID
API_HASH = '65e1f714a47c0879734553dc460e98d6'  # Replace with your API hash

# Use a string session or set to None for phone login
SESSION_STRING = None  # or put your session string here

# DC1 IP address and port
DC1_ID = 1
DC1_IP = '149.154.175.50'
DC1_PORT = 443

async def main():
    if SESSION_STRING:
        session = StringSession(SESSION_STRING)
    else:
        session = StringSession()

    client = TelegramClient(session, API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        print("Logging in...")
        await client.send_code_request(input("Enter your phone number: "))
        await client.sign_in(code=input("Enter the code you received: "))

    # Forcefully switch to DC1
    print(f"Changing session to DC1...")
    client.session.set_dc(dc_id=DC1_ID, server_address=DC1_IP, port=DC1_PORT)
    client.session.save()

    # Disconnect and reconnect to apply new DC
    await client.disconnect()
    await client.connect()

    # Get current session DC ID
    current_dc = client.session.dc_id
    print(f"Current DC ID: {current_dc}")

    if current_dc == DC1_ID:
        print("✅ Successfully connected to DC1.")
    else:
        print("❌ Not connected to DC1.")

    await client.disconnect()

asyncio.run(main())
  
