from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    # DATABASE_URL: str = "postgressql+asyncpg://user:password@host/dbname"
    DATABASE_URL: str = "postgresql+psycopg://postgres:root@localhost:5432/fastapi_ecom"
    # TODO Database url need to move to .env file when uploading to docker
    SECRET_KEY: str
    ALGORITHM: str

    model_config = { #pydantic v2
        "env_file": ".env",
        # "extra": "ignore",  # prevents 'Extra inputs not permitted'
    }

settings = Setting()