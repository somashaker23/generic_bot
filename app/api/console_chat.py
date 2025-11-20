from app.connector.console_connector import ConsoleConnector
from app.services.conversation_flow import ConversationFlow
from app.services.knowledge_engine import KnowledgeEngine


def start_console_chat():
    connector = ConsoleConnector()
    faq_engine = KnowledgeEngine()
    flow = ConversationFlow()

    print("Console Bot Chat Started (type 'exit' to stop)\n")

    while True:
        user_text = input("YOU: ")

        if user_text.lower() in ["exit", "quit"]:
            print("\nExiting console chat.")
            break

        # 1. FAQ
        faq_reply = faq_engine.search(user_text)
        if faq_reply:
            connector.send_message("console_user", faq_reply)
            continue

        # 2. Intent flow
        result = flow.process("user_id-1", user_text)
        connector.send_message("console_user", result["reply"])
