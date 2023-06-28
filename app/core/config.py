from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str = 'SECRET'
    postgres_db: str = 123
    postgres_user: str = 123
    postgres_password: str = 123
    db_host: str = 'localhost'
    db_port: str = 5000
    log_level: str = "WARNING"
    log_compression: str = "tar.gz"
    log_location: str = "logs/warning.log"
    log_rotation_time: str = '1 week'
    @property
    def database_url(self) -> str:
        """Получить ссылку для подключения к DB."""
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
