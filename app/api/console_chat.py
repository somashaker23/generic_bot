from app.connector.console_connector import ConsoleConnector
from app.services.conversation_flow import ConversationFlow


def start_console_chat():
    connector = ConsoleConnector()
    flow = ConversationFlow()

    print("Console Bot Chat Started (type 'exit' to stop)\n")

    while True:
        user_text = input("YOU: ")

        if user_text.lower() in ["exit", "quit"]:
            print("\nExiting console chat.")
            break

        #  Intent flow
        result = flow.process("user_id-1", user_text)
        connector.send_message("console_user", result["reply"])
