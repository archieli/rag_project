from src.query.query_engine import create_query_engine
from loguru import logger

if __name__=='__main__':
    query = 'What did the author do growing up?'
    query_engine = create_query_engine(folder_path='essay')
    rsp = query_engine.query(query)

    logger.info(f'问题: {query}')
    logger.info(f'回答: {rsp}')