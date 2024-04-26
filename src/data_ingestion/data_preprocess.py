from dataclasses import dataclass
from loguru import logger
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

@dataclass
class DataNode():
    '''This class is used to load the data from the directory and return the nodes
    '''
    folder_path: str
    node_name: str

    def __post_init__(self, folder_path: str='essay'):
        self.folder_path = folder_path
        self.nodes = self.directory_to_nodes(folder_path)

    def directory_to_nodes(self, folder_path: str):
        ''' Loads the data from the directory and returns the nodes
        '''
        documents = SimpleDirectoryReader(f"./data/{folder_path}").load_data()  #加载指定目录下的数据，生成 Document对象列表
        parser = SentenceSplitter()
        nodes = parser.get_nodes_from_documents(documents)  #将Document对象列表按句子划分，转换为Node对象列表

        return nodes
