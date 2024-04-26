from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core import PromptTemplate
from src.retriever.retriever import index_nodes
def update_prompts_for_query_engine(query_engine: BaseQueryEngine) -> BaseQueryEngine:

    new_tmpl_str = (
        "Below is the specific context required to answer the upcoming query. You must base your response solely on this context, strictly avoiding the use of external knowledge or assumptions..\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given this context, please formulate your response to the following query. Ensure your response adheres to these instructions to maintain accuracy and relevance."
        "Furthermore, it is crucial to respond in the same language in which the query is presented. This requirement is to ensure the response is directly applicable and understandable in the context of the query provided."
        "Query: {query_str}\n"
        "Answer: "
    )
    new_tmpl = PromptTemplate(new_tmpl_str)
    query_engine.update_prompts({"response_synthesizer:text_qa_template": new_tmpl})
    return query_engine

def create_query_engine(
    folder_path: str = "essay",
    embedding_model: str = "text-embedding-ada-002",
    similarity_top_k: int = 5,
) -> BaseQueryEngine:
    """ Create a Llama index query engine with the given configuration.
    """
    index = index_nodes(folder_path=folder_path, embedding_model=embedding_model)
    query_engine = index.as_query_engine(similarity_top_k=similarity_top_k)
    query_engine = update_prompts_for_query_engine(query_engine)
    return query_engine

