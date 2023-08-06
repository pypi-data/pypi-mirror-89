from fast_microservice.application import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8888, log_level="info", reload=True)
