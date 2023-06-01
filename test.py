from langchain.text_splitter import RecursiveCharacterTextSplitter

from EUDirective import EUDirective

directive = EUDirective('dlt_pilot.html')

data = directive.get_documents()

splitter = RecursiveCharacterTextSplitter(chunk_size = 25, chunk_overlap = 5)

texts = splitter.split_documents(data)

print(texts[0])
print(texts[1])
print(texts[2])