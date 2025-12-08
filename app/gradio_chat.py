import gradio as gr

from app.services.conversation_flow import ConversationFlow

flow = ConversationFlow()


def gradio_handler(message, history):
    """
    Wrap your ConversationFlow class into a Gradio-compatible function.
    """
    user_id = "gradio_user"  # You can replace this with session_id later
    result = flow.handle_message(user_id, message)
    return result["reply"]  # Gradio only expects the text reply


def get_gradio_app():
    """
    Returns a Gradio ChatInterface instance.
    """
    dark = gr.themes.Base().set(
        body_background_fill="#0f0f0f",
        body_text_color="#e5e5e5",
        block_background_fill="#1a1a1a",
        block_title_text_color="#ffffff",
        link_text_color="#8ab4f8",
    )

    chatbot = gr.Chatbot(
        height=600,
        layout="bubble",
        avatar_images=(None, None),  # add your custom chat avatars here
    )
    return gr.ChatInterface(
        fn=gradio_handler,
        title="Car Assistant (Dark Mode)",
        chatbot=chatbot,
        examples=[
            "I want to book a test drive for the creta.",
            "How much is the creta?",
            "When is the earliest service slot available?",
        ],
        example_labels=["Test Drive", "Pricing", "Service"],
        run_examples_on_click=True,

    )
