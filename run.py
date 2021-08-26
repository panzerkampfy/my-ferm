import uvicorn

if __name__ == "__main__":
    uvicorn.run("core.main:app", host="localhost", port=9091, log_level="info")
