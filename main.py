from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

api_id = 18136872  # Replace with your real API ID
api_hash = '312d861b78efcd1b02183b2ab52a83a4'  # Replace with your real API Hash

async def main():
    print("== Telegram Message Reporter ==")

    phone = input("Enter your phone number (with +91...): ")

    # Start temporary client session
    client = TelegramClient(StringSession(), api_id, api_hash)

    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input("Enter the code you received: ")
        await client.sign_in(phone, code)

    # Get the chat link or username
    target = input("Enter the username or chat link of the sender: ").strip()
    msg_id = int(input("Enter the message ID to report: ").strip())

    # Resolve entity
    try:
        peer = await client.get_entity(target)
    except Exception as e:
        print("Error finding user/chat:", e)
        await client.disconnect()
        return

    try:
        message = await client.get_messages(peer, ids=msg_id)
    except Exception as e:
        print("Could not fetch message:", e)
        await client.disconnect()
        return

    # Show message details
    print("\n== Message Details ==")
    print(f"Message ID: {message.id}")
    print(f"Sender ID: {message.sender_id}")
    print(f"Date: {message.date}")
    print(f"Content:\n{message.text or '[No text]'}")

    confirm = input("\nDo you want to report this message? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        await client.disconnect()
        return

    try:
        report = await client(functions.messages.ReportRequest(
            peer=peer,
            id=[msg_id],
            reason=types.InputReportReasonViolence(),  # You can change the reason
            message="report: offensive content."
        ))
        print("✅ Report submitted:", report)
    except Exception as e:
        print("❌ Failed to report:", e)

    await client.disconnect()

# ------------- Run it -------------
import asyncio
asyncio.run(main())
