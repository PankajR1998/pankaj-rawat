from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_core.runnables.passthrough import RunnablePassthrough
from dotenv import load_dotenv
import os,time
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains.llm import LLMChain
# load_dotenv()


class RAG:
    def __init__(self):
        # self.posts = posts
        self.prompt_template = """
    ### [INST] 
    Instruction: Answer the question (without any extra text) based on your 
    knowledge about the context. Here is context to help:

    {context}

    ### QUESTION:
    {question} 

    [/INST]
    """
    
    def load_env_variables(self):
        load_dotenv()
        return True
    def preprocessing(self,context):
        documents = [Document(page_content=post) for post in context]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000,chunk_overlap=10000)
        documents = text_splitter.split_documents(documents=documents)
        return documents
    def vector_conversion_retrieval(self,documents):
        start = time.time()
        embedding = HuggingFaceEmbeddings()
        db = FAISS.from_documents(documents, embedding=embedding)
        retriever = db.as_retriever()
        print("Time taken to store in vector store:",round(time.time()-start))
        return retriever
    
    def rag_chaining(self,retriever):
        prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=self.prompt_template,
    )
        model_name = 'mistralai/Mistral-7B-Instruct-v0.2'
        model = HuggingFaceEndpoint(endpoint_url=model_name,task="text-generation")
        llmchain=LLMChain(llm=model,prompt=prompt)

        rag_chain = ( 
        {"context": retriever, "question": RunnablePassthrough()}
            | llmchain
        )
        return rag_chain
    def result(self,chain,query:str):
        result = chain.invoke(input=query)
        return result['text']



        



if __name__=="__main__":
    query = "what are the misuses of GenAI?"
    # print(generting_rag_answer(query=query))
    rag = RAG()
    rag.load_env_variables()
    docs = rag.preprocessing()
    retriever = rag.vector_conversion_retrieval(documents=docs)
    rag_chain = rag.rag_chaining(retriver=retriever)
    print(rag.result(rag_chain))


