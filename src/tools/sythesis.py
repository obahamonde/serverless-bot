from typing import List, Literal, Optional

from boto3 import Session
from pydantic import BaseModel, Field


class PollySynthesizeSpeechInput(BaseModel):
    Engine: Literal["standard", "neural"] = Field("standard", description="Specifies the engine for Amazon Polly to use when processing input text for speech synthesis.")
    LanguageCode: Optional[str] = Field(None, description="Optional language code for the Synthesize Speech request.")
    LexiconNames: Optional[List[str]] = Field(None, description="List of one or more pronunciation lexicon names you want the service to apply during synthesis.")
    OutputFormat: Literal["json", "mp3", "ogg_vorbis", "pcm"] = Field("mp3", description="The format in which the returned output will be encoded.")
    SampleRate: str = Field("22050", description="The audio frequency specified in Hz.")
    SpeechMarkTypes: Optional[List[Literal["sentence", "ssml", "viseme", "word"]]] = Field(None, description="The type of speech marks returned for the input text.")
    Text: str = Field(..., description="Input text to synthesize.")
    TextType: Literal["ssml", "text"] = Field("text", description="Specifies whether the input text is plain text or SSML.")
    VoiceId: Literal["Aditi", "Amy", "Astrid", "Bianca", "Brian", "Camila", "Carla", "Carmen", "Celine", "Chantal", "Conchita", "Cristiano", "Dora", "Emma", "Enrique", "Ewa", "Filiz", "Gabrielle", "Geraint", "Giorgio", "Gwyneth", "Hans", "Ines", "Ivy", "Jacek", "Jan", "Joanna", "Joey", "Justin", "Karl", "Kendra", "Kevin", "Kimberly", "Lea", "Liv", "Lotte", "Lucia", "Lupe", "Mads", "Maja", "Marlene", "Mathieu", "Matthew", "Maxim", "Mia", "Miguel", "Mizuki", "Naja", "Nicole", "Olivia", "Penelope", "Raveena", "Ricardo", "Ruben", "Russell", "Salli", "Seoyeon", "Takumi", "Tatyana", "Vicki", "Vitoria", "Zeina", "Zhiyu", "Aria", "Ayanda", "Arlet", "Hannah", "Arthur", "Daniel", "Liam", "Pedro", "Kajal", "Hiujin", "Laura", "Elin", "Ida", "Suvi", "Ola", "Hala", "Andres", "Sergio", "Remi", "Adriano", "Thiago", "Ruth", "Stephen", "Kazuha", "Tomoko", "Niamh", "Sofie"] = Field(..., description="Voice ID to use for the synthesis. Each voice speaks a specific language. For example, 'Aditi' speaks Indian English and Hindi, 'Amy' speaks British English, 'Astrid' speaks Swedish, 'Bianca' speaks Italian, and so on.")

