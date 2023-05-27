from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)

text = "Give an enthusiastic introduction to BigBot, the ChatGPT based bot helping cute EU bureaucrats in finding relevant passages from Eur Lex"
print(llm(text))