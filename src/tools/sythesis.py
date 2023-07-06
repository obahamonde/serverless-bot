from io import BytesIO
from typing import List, Literal, Optional

from boto3 import Session
from pydantic import BaseModel, Field


class Polly(BaseModel):
    Engine: Literal["standard", "neural"] = Field(default="standard", description="Specifies the engine for Amazon Polly to use when processing input text for speech synthesis.")
    LanguageCode: Optional[str] = Field(default=None, description="Optional language code for the Synthesize Speech request.")
    LexiconNames: Optional[List[str]] = Field(default=None, description="List of one or more pronunciation lexicon names you want the service to apply during synthesis.")
    OutputFormat: Literal["json", "mp3", "ogg_vorbis", "pcm"] = Field(default="mp3", description="The format in which the returned output will be encoded.")
    SampleRate: str = Field(default="22050", description="The audio frequency specified in Hz.")
    SpeechMarkTypes: Optional[List[Literal["sentence", "ssml", "viseme", "word"]]] = Field(default=None, description="The type of speech marks returned for the input text.")
    Text: str = Field(..., description="Input text to synthesize.")
    TextType: Literal["ssml", "text"] = Field(default="text", description="Specifies whether the input text is plain text or SSML.")
    VoiceId: str = Field(default="Mia", description="Voice ID to use for the synthesis.")

    @classmethod
    def from_text(cls,text:str):
        return cls(Text=text)


    @property
    def client(self):
        return Session().client("polly", region_name="us-east-1")
    
    @property
    def s3(self):
        return Session().client("s3", region_name="us-east-1")
    
    
    def synthesize(self):
        return self.client.synthesize_speech(**self.dict(exclude_none=True))
    
    def get_audio(self):
        byte_stream = BytesIO()
        with self.synthesize()["AudioStream"] as stream:
            byte_stream.write(stream.read())
        byte_stream.seek(0)
        return byte_stream
    
    def upload_audio(self, bucket: str, key: str):
        self.s3.upload_fileobj(self.get_audio(), bucket, key)
        return f"https://s3.amazonaws.com/{bucket}/{key}"
    
