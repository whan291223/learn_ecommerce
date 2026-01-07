from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    # DATABASE_URL: str = "postgressql+asyncpg://user:password@host/dbname"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    STRIPE_SECRET_KEY: str
    model_config = { #pydantic v2
        "env_file": ".env",
        # "extra": "ignore",  # prevents 'Extra inputs not permitted'
    }

settings = Setting()