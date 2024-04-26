from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from loguru import logger

from src.data_ingestion.data_preprocess import DataNode


def index_nodes(folder_path: str, embedding_model: str='text-embedding-ada-002'):
    ''' 将指定目录下的所有文件，解析成数据块后构建索引
    '''
    collection_name = f'{folder_path}_index'
    data_nodes = DataNode(folder_path, collection_name) #生成数据块

    client = QdrantClient("localhost", port=6333)
    try:
        count = client.count(collection_name).count
    except UnexpectedResponse:
        count = 0

    embed_model = OpenAIEmbedding(model=embedding_model)
    if count == len(data_nodes.nodes):  #已经构建过索引，直接返回
        logger.info(f"Found {count} existing nodes. Using the existing collection.")
        vector_store = QdrantVectorStore(
            collection_name=collection_name,
            client=client,
        )
        return VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embed_model,
        )
    logger.info(f"Found {count} existing nodes. Creating a new index with {len(data_nodes.nodes)} nodes. This may take a while.")
    if count > 0:   #删除已有的索引，准备重构索引
        client.delete_collection(collection_name)

    vector_store = QdrantVectorStore(
        collection_name=collection_name,
        client=client,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(
        data_nodes.nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    return index
