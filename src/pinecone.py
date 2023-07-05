

from .config import *
from .lib import *
from .models import *
from .typedefs import *


class PineConeSparsedValues(BaseModel):
    """
    A class used to represent the sparsed values of a Pinecone vector.

    Attributes
    ----------
    indices : List[int]
        The indices of the embedding.
    values : Vector
        The values of the embedding.
    """

    indices: List[int] = Field(..., description="The indices of the embedding.")
    values: Vector = Field(..., description="The values of the embedding.")


class PineconeVector(BaseModel):
    """
    A class used to represent a Pinecone vector.

    Attributes
    ----------
    id : str
        The ID of the embedding.
    values : Vector
        The values of the embedding.
    sparseValues : Optional[PineConeSparsedValues]
        The sparse values of the embedding.
    metadata : Metadata
        The metadata of the embedding. Must be a dictionary of strings.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="The ID of the embedding."
    )
    values: Vector = Field(..., description="The values of the embedding.")
    sparseValues: Optional[PineConeSparsedValues] = Field(
        default_factory=list, description="The sparse values of the embedding."
    )
    metadata: Context = Field(
        default_factory=dict,
        description="The metadata of the embedding. Must be a dictionary of strings.",
    )


class PineconeVectorUpsert(BaseModel):
    """
    A class used to represent an upsert operation on a Pinecone vector.

    Attributes
    ----------
    namespace : str
        The namespace of the embedding.
    vectors : List[PineconeVector]
        The vectors of the embedding.
    """

    namespace: str = Field(..., description="The namespace of the embedding.")
    vectors: List[PineconeVector] = Field(
        ..., description="The vectors of the embedding."
    )


class PineconeVectorQuery(BaseModel):
    """
    A class used to represent a query on a Pinecone vector.

    Attributes
    ----------
    namespace : str
        The namespace of the embedding.
    topK : int
        The number of results to return.
    vector : Vector
        The vector of the embedding.
    """

    namespace: str = Field(..., description="The namespace of the embedding.")
    topK: int = Field(default=8, description="The number of results to return.")
    vector: Vector = Field(..., description="The vector of the embedding")


class PineconeVectorMatch(BaseModel):
    """
    A class used to represent a match of a Pinecone vector.

    Attributes
    ----------
    id : str
        The ID of the embedding.
    score : float
        The score of the embedding.
    values : Vector
        The vector of the embedding.
    sparseValues : Optional[PineConeSparsedValues]
        The sparse values of the embedding.
    metadata : Optional[Metadata]
        The metadata of the embedding.
    """

    id: str = Field(..., description="The ID of the embedding.")
    score: float = Field(..., description="The score of the embedding.")
    values: Optional[Vector] = Field(None, description="The vector of the embedding.")
    sparseValues: Optional[PineConeSparsedValues] = Field(
        None, description="The sparse values of the embedding."
    )
    metadata: Optional[Context] = Field(default=None,
                                        description="The metadata of the embedding.")


class PineconeVectorResponse(BaseModel):
    """
    A class used to represent a response from a Pinecone vector request.

    Attributes
    ----------
    matches : List[PineconeVectorMatch]
        The matches of the embedding.
    namespace : str
        The namespace of the embedding.
    """

    matches: List[PineconeVectorMatch] = Field(
        ..., description="The matches of the embedding."
    )
    namespace: str = Field(..., description="The namespace of the embedding.")


headers = {
    "Content-Type": "application/json",
    "api-key": env.PINECONE_API_KEY,
}


class PineConeClient(ApiClient):
    """
    A client for interacting with the Pinecone API.

    Attributes
    ----------
    base_url : str
        The base URL for the Pinecone API. This is set from the environment variable PINECONE_API_URL.
    headers : dict
        The headers to include with each API request. This includes the Content-Type and the API key, which is set from the environment variable PINECONE_API_KEY.

    Methods
    -------
    async upsert(request: PineconeVectorUpsert) -> None:
        Upserts a vector to the Pinecone service. The vector is defined in the `PineconeVectorUpsert` request object.
        This method sends a POST request to the "/vectors/upsert" endpoint of the Pinecone API.

    async query(request: PineconeVectorQuery) -> PineconeVectorResponse:
        Queries the Pinecone service with a vector. The vector is defined in the `PineconeVectorQuery` request object.
        This method sends a POST request to the "/query" endpoint of the Pinecone API and returns a `PineconeVectorResponse` object.
    """

    async def upsert(self, request: PineconeVectorUpsert) -> None:
        await self.fetch(
            "https://llmtoolmvp-8360578.svc.us-central1-gcp.pinecone.io/vectors/upsert",
            "POST",
            headers,
            request.dict(),
        )

    async def query(self, request: PineconeVectorQuery):
        response = await self.fetch(
            "https://llmtoolmvp-8360578.svc.us-central1-gcp.pinecone.io/query",
            "POST",
            headers,
            request.dict(),
        )
        assert isinstance(response, dict)
        return PineconeVectorResponse(**response)

    async def get_context(self, namespace: str, text: str, vector: Vector):
        query_ = PineconeVectorQuery(namespace=namespace, vector=vector)
        upsert_ = PineconeVectorUpsert(
            namespace=namespace,
            vectors=[PineconeVector(values=vector, metadata={"text": text})]
        )
        query_response = await self.query(query_)
        await self.upsert(upsert_)
        vector_models = query_response.matches
        return [vector_model.metadata for vector_model in vector_models]
