import logging
import os
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

logger = logging.getLogger("scanman")


def load_retriever(manpage):
    db_path = os.path.join(os.path.expanduser("~"), ".scanman", "embeddings", manpage.name, "embeddings.db")

    # Load if previously calculated
    if os.path.exists(db_path):
        db = FAISS.load_local(
            db_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True
        )
        logger.info(f"Loaded embeddings for `{manpage.name}` from {db_path}...")

        return db.as_retriever()

    # Otherwise calculate
    else:
        docs = [Document(page_content=manpage.content())]
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        docs = splitter.split_documents(docs)

        db = FAISS.from_documents(docs, OpenAIEmbeddings())
        db.save_local(db_path)
        logger.info(f"Created and saved embeddings for `{manpage.name}` to {db_path}.")

        return db.as_retriever()


def ask(query, state):
    llm = ChatOpenAI(temperature=0)
    doc_combiner = create_stuff_documents_chain(
        llm, hub.pull("langchain-ai/retrieval-qa-chat")
    )

    # `retriever` is set to `None` after manpage change.
    if state.retriever is None:
        state.retriever = load_retriever(state.manpage)

    chain = create_retrieval_chain(state.retriever, doc_combiner)

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

        Use the following context: {state.memory.chat_memory}
        """
    )
    template = ChatPromptTemplate.from_messages(
        [("system", system_message), ("human", "{query}")]
    )
    prompt = template.invoke({"query": query})

    return chain.invoke({"input": prompt.to_string()})
