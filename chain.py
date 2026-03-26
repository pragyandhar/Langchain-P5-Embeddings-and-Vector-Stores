from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# Prompt
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions based on provided context.
    If the answer is not found in the context, say 
    "I could not find this in the document." 
    Do not use any outside knowledge.
    Context:
    {context}"""),

    ("human", "{question}")
])

def format_documents(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def build_chain(retriever):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chain = (
        RunnablePassthrough.assign(
            context = RunnableLambda(lambda x: x['question']) | retriever | RunnableLambda(format_documents)
        )
        | prompt_template
        | llm
        | StrOutputParser()
    )

    return chain
