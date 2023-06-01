from langchain.document_loaders import UnstructuredHTMLLoader

from EUDirective import EUDirective

directive = EUDirective('dlt_pilot.html')

loader = UnstructuredHTMLLoader('dlt_pilot.html')

data = loader.load()

print(data)