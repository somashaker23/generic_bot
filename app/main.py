from fastapi import FastAPI

# Create FastAPI app instance
app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}
