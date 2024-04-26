# rag_project
RAG的技术研究及相关项目

1. 安装Docker并在本地启动
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant

   
2. 设置OpenAI的key
export OPENAI_API_KEY=sk-
