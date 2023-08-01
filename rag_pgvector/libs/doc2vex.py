
from sagemaker.session import Session
# from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

from sagemaker_embeddings_model import SagemakerEmbeddingsModel

TIKTOKEN_ENCODING = 'p50k_base'
TEXT_EMBEDDING_ENDPOINT = ""

class DocToVex:

    def __init__(self, sm_session=None, embedding_endpoint=TEXT_EMBEDDING_ENDPOINT, token_encoding=TIKTOKEN_ENCODING) -> None:
        print('instancing sagemaker session')
        if sm_session is None:
            self.sagemaker_session = Session()
        else: 
            self.sagemaker_session = sm_session
        
        # setup the tokenizer 
        print(f'instancing tokenizer for "{token_encoding}" encoding')
        self.tokenizer = tiktoken.get_encoding(token_encoding)
        # setup the embedder model
        print('instancing the text embedding model')
        self.embedder = SagemakerEmbeddingsModel(embedding_endpoint, self.sagemaker_session)

    def get_token_length(self, text):
        tokens = self.tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)

    def get_page_chunks(self, page_content, chunk_size=200, chunk_overlap=20):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function = self.get_token_length,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_text(page_content)
        return chunks
    
    def get_text_embedding(self, text):
        return self.embedder.query_endpoint(text)
    
    def get_document_vectors(self, content, chunk_size=200, chunk_overlap=20):
        # divide the content into 200 token chunks
        chunks = self.get_page_chunks(content, chunk_size, chunk_overlap)
        print(f"Found {len(chunks)} chunks")

        # iterate through page chunks and vectorize them
        doc_vecs = []
        for i, chunk in enumerate(chunks):
            # print(f"embed chunk {i}")
            vec = self.get_text_embedding(chunk)
            doc_vecs.append(vec)
            # print(f'generated {len(doc_vecs)} vectors from input doc')
        
        return (chunks, doc_vecs) 
    
