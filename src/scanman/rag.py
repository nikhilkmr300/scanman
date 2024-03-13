import textwrap

from langchain import hub
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


ERROR_MSG = "I'm sorry, I don't know."


def load_retriever(manpage):
    docs = [Document(page_content=manpage.content())]
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = splitter.split_documents(docs)
    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    return db.as_retriever()


def ask(query, retriever, memory):
    llm = ChatOpenAI(temperature=0)
    doc_combiner = create_stuff_documents_chain(
        llm, hub.pull("langchain-ai/retrieval-qa-chat")
    )
    chain = create_retrieval_chain(retriever, doc_combiner)

    system_message = textwrap.dedent(
        f"""\
        You are a helpful assistant that retrieves information from UNIX
        man pages. Your name is "scanman".

        Obey the following rules:
        * Always remain polite and helpful.
        * Appropriately respond to greetings. Add a helpful message about the
          questions that you may be asked.
        * Appropriately respond to questions about yourself and expectations of
          you.
        * If the user asks you something that is not relevant to the current man
          page, respond with "{ERROR_MSG}". Use this option **very** sparingly
          and try to bring the conversation back to questions about the man
          page.

        Use the following context: {memory.chat_memory}
        """
    )
    template = ChatPromptTemplate.from_messages(
        [("system", system_message), ("human", "{query}")]
    )
    prompt = template.invoke({"query": query})
    return chain.invoke({"input": prompt.to_string()})
