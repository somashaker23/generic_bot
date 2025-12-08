import gradio as gr
from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.webhook_router import router as whatsapp_webhook
from app.gradio_chat import get_gradio_app

app = FastAPI()

app.include_router(health_router, prefix="", tags=["health"])
app.include_router(whatsapp_webhook, prefix="/webhook", tags=["whatsapp"])


gradio_app = get_gradio_app()
app = gr.mount_gradio_app(app, gradio_app, path="/ui")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
# from app.api.console_chat import start_console_chat
#
# if __name__ == "__main__":
#     start_console_chat()
