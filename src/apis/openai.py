from ..config import env
from ..models import *
from ..tools import *


class OpenAIEmbeddingRequest(BaseModel):
    """
    A class used to represent a request for an OpenAI embedding.

    Attributes
    ----------
    model : str
        The model to be used for the embedding. Default is "text-embedding-ada-002".
    input : str
        The text to be embedded.
    namespace: str
        The namespace of the embedding.
    """

    model: str = Field(default="text-embedding-ada-002")
    input: str = Field(..., description="The text to embed")
    namespace: str = Field(..., description="The namespace of the embedding.")


class OpenAIEmbeddingObject(BaseModel):
    """
    A class used to represent an OpenAI embedding object.

    Attributes
    ----------
    object : str
        The string 'embedding'.
    index : int
        The index of the input.
    embedding : Vector
        The embedding of the input.
    """

    object: str = Field(..., description="The string 'embedding'.")
    index: int = Field(..., description="The index of the input.")
    embedding: Vector = Field(..., description="The embedding of the input.")


class OpenAIEmbeddingUsage(BaseModel):
    """
    A class used to represent the usage of an OpenAI embedding.

    Attributes
    ----------
    prompt_tokens : int
        The number of tokens in the prompt.
    total_tokens : int
        The total number of tokens generated by the engine.
    """

    prompt_tokens: int = Field(..., description="The number of tokens in the prompt.")
    total_tokens: int = Field(
        ..., description="The total number of tokens generated by the engine."
    )


class OpenAIEmbeddingResponse(BaseModel):
    """
    A class used to represent a response from an OpenAI embedding request.

    Attributes
    ----------
    object : str
        The string 'list'.
    data : List[OpenAIEmbeddingObject]
        The list of embeddings, in the same order as the input list.
    model : str
        The model used to generate the embeddings.
    usage : OpenAIEmbeddingUsage
        The object containing information about the model's resource usage.
    """

    object: str = Field(..., description="The string 'list'.")
    data: List[OpenAIEmbeddingObject] = Field(
        ..., description="The list of embeddings, in the same order as the input list."
    )
    model: str = Field(..., description="The model used to generate the embeddings.")
    usage: OpenAIEmbeddingUsage = Field(
        ...,
        description="The object containing information about the model's resource usage.",
    )


class OpenAIChatCompletionMessage(BaseModel):
    """
    A class used to represent a message in a chat completion.

    Attributes
    ----------
    role : Literal["system", "user", "assistant"]
        Role of the message.
    content : str
        Content of the message.
    """

    role: Literal["system", "user", "assistant"] = Field(
        ..., description="Role of the message"
    )
    content: str = Field(..., description="Content of the message")


class OpenAIChatGptRequest(BaseModel):
    """
    A class used to represent a request to the OpenAI GPT model for chat completion.

    Attributes
    ----------
    model : str
        The ID of the engine to use for completion.
    messages : List[OpenAIChatCompletionMessage]
        Pair of messages from system and human.
    temperature : float
        What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).
    max_tokens : int
        The maximum number of tokens to generate. Requests can use up to 2048 tokens shared between prompt and completion.
    top_p : float
        An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    frequency_penalty : float
        What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).
    presence_penalty : float
        What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).
    n : int
        The number of completions to generate for each prompt.
    """

    model: str = Field(
        default="gpt-3.5-turbo-16k-0613",
        description="The ID of the engine to use for completion.",
    )
    messages: List[OpenAIChatCompletionMessage] = Field(
        default=[], description="Pair of messages from system and human", max_items=2
    )
    temperature: float = Field(
        default=0.75,
        description="What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).",
    )
    max_tokens: int = Field(
        default=2048,
        description="The maximum number of tokens to generate. Requests can use up to 2048 tokens shared between prompt and completion.",
    )
    top_p: float = Field(
        default=1.0,
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
    )
    frequency_penalty: float = Field(
        default=0.25,
        description="What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).",
    )
    presence_penalty: float = Field(
        default=0.25,
        description="What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).",
    )
    n: int = Field(
        default=1, description="The number of completions to generate for each prompt."
    )

    def chain(self, content: str, prompt: str):
        self.messages = [
            OpenAIChatCompletionMessage(role="user", content=prompt),
            OpenAIChatCompletionMessage(
                role="assistant",
                content=content,
            ),
        ]
        return self


class OpenAIChatCompletionChoice(BaseModel):
    """
    A class used to represent a choice in a chat completion.

    Attributes
    ----------

    index : int
        The index of the choice that was selected by the model.
    message : OpenAIChatCompletionMessage
        The text of the choice that was selected by the model.
    finish_reason : str
        The reason the conversation ended. This will be completion, api_call, or timeout.
    """

    index: int = Field(
        ..., description="The index of the choice that was selected by the model."
    )
    message: OpenAIChatCompletionMessage = Field(
        ..., description="The text of the choice that was selected by the model."
    )
    finish_reason: str = Field(
        ...,
        description="The reason the conversation ended. This will be completion, api_call, or timeout.",
    )


class OpenAIChatCompletionUsage(BaseModel):
    """
    A class used to represent the resource usage of a chat completion.

    Attributes
    ----------

    prompt_tokens : int
        The number of tokens in the prompt.
    completion_tokens : int
        The number of tokens in the completion.
    total_tokens : int
        The total number of tokens generated by the engine.
    """

    prompt_tokens: int = Field(..., description="The number of tokens in the prompt.")
    completion_tokens: int = Field(
        ..., description="The number of tokens in the completion."
    )
    total_tokens: int = Field(
        ..., description="The total number of tokens generated by the engine."
    )


class OpenAIChatCompletionResponse(BaseModel):
    """
    A class used to represent a response from the OpenAI GPT model for chat completion.

    Attributes
    ----------

    id : str
        The unique identifier for the completion.
    object : str
        The string 'text_completion'.
    created : int
        When the prompt was created (UNIX timestamp).
    choices : List[OpenAIChatCompletionChoice]
        The list of choices the engine made, in chronological order.
    usage : OpenAIChatCompletionUsage
        The object containing information about the model's resource usage.
    """

    id: str = Field(..., description="The unique identifier for the completion.")
    object: str = Field(..., description="The string 'text_completion'.")
    created: int = Field(
        ..., description="When the prompt was created (UNIX timestamp)."
    )
    choices: List[OpenAIChatCompletionChoice] = Field(
        ..., description="The list of choices the engine made, in chronological order."
    )
    usage: OpenAIChatCompletionUsage = Field(
        ...,
        description="The object containing information about the model's resource usage.",
    )


class OpenAIChatCompletionRequest(BaseModel):
    """
    A class used to represent a request to the OpenAI GPT model for chat completion.

    Attributes
    ----------

    namespace:
        The namespace of the website inside the Vector database
    prompt:
        The prompt to send to the AI
    context:
        The context to send to the AI
    role:
        The role that the chatbot should play
    """

    namespace: str = Field(
        ..., description="The namespace of the website inside the Vector database"
    )
    prompt: str = Field(..., description="The prompt to send to the AI")
    context: Context = Field(..., description="The context to send to the AI")
    role: str = Field(..., description="The role that the chatbot should play")

    def chain(self):
        return LeadsTemplate(self)


class OpenAIPineConeRequest(BaseModel):
    """
    A class used to represent a request to the OpenAI GPT model for chat completion.

    Attributes
    ----------

    namespace:
        The namespace of the website inside the Vector database
    vector:
        The vector to send to the AI
    """

    namespace: str = Field(
        ..., description="The namespace of the website inside the Vector database"
    )
    vector: Vector = Field(..., description="The vector to send to the AI")


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {env.OPENAI_API_KEY}",
}


class OpenAIClient(ApiClient):
    async def post_embeddings(
        self, request: OpenAIEmbeddingRequest
    ) -> OpenAIEmbeddingResponse:
        response = await self.fetch(
            "https://api.openai.com/v1/embeddings", "POST", headers, request.dict()
        )
        assert isinstance(response, dict)
        return OpenAIEmbeddingResponse(**response)

    async def retrieve_context(self, request: OpenAIEmbeddingRequest):
        response = await self.fetch(
            "https://api.openai.com/v1/embeddings", "POST", headers, request.dict()
        )
        assert isinstance(response, dict)
        embedding_response = OpenAIEmbeddingResponse(**response)
        vector = embedding_response.data[0].embedding
        namespace = request.namespace
        return OpenAIPineConeRequest(namespace=namespace, vector=vector)

    async def text_completion(
        self, request: OpenAIChatGptRequest
    ) -> OpenAIChatCompletionResponse:
        response = await self.fetch(
            "https://api.openai.com/v1/chat/completions",
            "POST",
            headers,
            request.dict(),
        )
        assert isinstance(response, dict)
        return OpenAIChatCompletionResponse(**response)
