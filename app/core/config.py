from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Получение информации о товарах с WB"
    redis_url: str
    api_url: str
    api_token: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()
