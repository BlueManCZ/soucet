import dotenv
import os
import redis

dotenv.load_dotenv()

REDIS_URL = "redis://localhost"
redis_session = redis.from_url(REDIS_URL)
redis_session.ping()


class ApplicationConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    # SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # SESSION_COOKIE_DOMAIN = False
    SESSION_REDIS = redis_session
