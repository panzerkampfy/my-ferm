import logging

from db.session import SessionLocal
from tenacity import retry, stop_after_attempt, wait_fixed

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        raise e


def main() -> None:
    init()


if __name__ == "__main__":
    main()
