from app.connector.console_connector import ConsoleConnector
from app.services.knowledge_engine import KnowledgeEngine
from app.services.intent_router import IntentRouter


def start_console_chat():
    connector = ConsoleConnector()
    faq_engine = KnowledgeEngine()
    intent_router = IntentRouter()

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
        result = intent_router.handle(user_text)
        connector.send_message("console_user", result["reply"])
