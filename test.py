import langchain

import nltk.data

from langchain.embeddings import FakeEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from EUDirective import EUDirective

from langchain.schema import Document

class SentenceSplitter(langchain.text_splitter.TextSplitter):
    def __init__(self, max_chunk_size=4000, chunk_overlap=200):
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.max_chunk_size = 4000
        self.chunk_overlap=200

    def split_text(self, documents):
        return [Document(page_content=s, metadata = d.metadata) for d in documents for s in self.tokenizer.tokenize(d)]

directive = EUDirective('dlt_pilot.html')

splitter = SentenceSplitter()

texts = splitter.split_documents(directive.get_documents())

query = """Phrases related to "union law" """

embeddings = FakeEmbeddings(size=1024)
docsearch = Chroma.from_texts([t.page_content for t in texts], embeddings, metadatas=[t.metadata for t in texts])

docs = docsearch.similarity_search(query)

print(docs)