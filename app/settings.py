from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Clase para cargar configuraciones desde variables de entorno utilizando Pydantic.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BALL_MODEL_PATH: str = "app/models/ball_yolo11.pt"
    PLAYER_MODEL_PATH: str = "app/models/player_yolo11.pt"

Settings = Settings()  # type: ignore
