from pydantic import BaseConfig, BaseSettings
from pydantic import Field as Data


class Env(BaseSettings):
    """Environment Variables"""

    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"

    FAUNA_SECRET: str = Data(..., env="FAUNA_SECRET")
    AUTH0_URL: str = Data(..., env="AUTH0_URL")
    OPENAI_API_KEY: str = Data(..., env="OPENAI_API_KEY")
    PINECONE_API_KEY: str = Data(..., env="PINECONE_API_KEY")
    PINECONE_API_URL: str = Data(..., env="PINECONE_API_URL")
    AWS_ACCESS_KEY_ID: str = Data(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY:str = Data(..., env="AWS_SECRET_ACCESS_KEY")
    REGION_NAME:str = Data(..., env="REGION_NAME")
    
    def __init__(self):
        super().__init__()


env = Env()
