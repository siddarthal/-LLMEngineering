from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import gradio as gr
from langchain_core.messages import HumanMessage, SystemMessage,convert_to_messages
from langchain_core.documents import Document
load_dotenv()
MODEL = "gpt-4.1-nano"
DB_NAME = "vector_db"

def generate_system_prompt(query):
    SYSTEM_PROMPT_TEMPLATE = f"""
    You are a knowledgeable, friendly assistant representing the company Insurellm.
    You are chatting with a user about Insurellm.
    If relevant, use the given context to answer any question.
    If you don't know the answer, say so.
    Context:
    {query}
    """
    return SYSTEM_PROMPT_TEMPLATE

def fetch_context(combinedq: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = Chroma(embedding_function=embeddings,persist_directory=DB_NAME)
    retriever = vector_store.as_retriever()
    return retriever.invoke(combinedq,k=10)

def get_llm():
    llm = ChatOpenAI(model=MODEL, temperature=0)
    return llm

def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question

def answer_question(question: str, history: list[dict] = []) -> tuple[str, list[Document]]:
    combinedq=str(combined_question(question, history))
    docs = fetch_context(combinedq)
    context ="\n\n".join(doc.page_content for doc in docs)
    sys_prompt = generate_system_prompt(context)
    messages = [SystemMessage(content=sys_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    response = get_llm().invoke(messages)
    return response.content,docs
