import os

class Config:
    # Redis settings
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = os.getenv("REDIS_DB", 0)

    # Celery settings
    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    # Celery beat settings
    CRONTAB = os.getenv("CRONTAB", "0 0 */1 * *").split() if len(os.getenv("CRONTAB", "0 0 */1 * *").split()) == 5 else "0 0 */1 * *".split()
    TIMEZONE = os.getenv("TIMEZONE", "UTC")

    # Azure connection
    AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
