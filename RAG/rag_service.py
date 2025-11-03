from fastapi import FastAPI, Body
from pybase16384.backends.cffi.build import system
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from sympy.physics.units import temperature
from sympy.stats.sampling.sample_numpy import numpy

app = FastAPI(title='RAG Service')
# 示例文本
texts = ["爆红是指在网络上迅速走红的现象", "社交媒体上的爆红内容通常具有传播性"]

CHROMA_DIR = os.getenv('CHROMA_DIR', "./chroma_data")
# 初始化嵌入模型
# embeddings = OpenAIEmbeddings(api_key="your-openai-api-key")
# 初始化 Chroma 向量存储
# vector_store = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")
# deepseek as openai-compatible
llm = ChatOpenAI(
    model="deepseek-chat",  # 例：deepseek-chat / deepseek-reasoner
    temperature=0.2,
    openai_api_base=os.getenv("DEEPSEEK_API_BASE"),
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    timeout=30,
)

emb = OpenAIEmbeddings(
    model="text-embedding-3-large",  # 如果 DeepSeek/部署有自家 embedding，也可替换
    openai_api_base=os.getenv("DEEPSEEK_API_BASE"),
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
)
vectordb = Chroma(
    collection_name="jobs_corpus",
    embedding_function=emb,
    persist_directory=CHROMA_DIR
)


class IngestItem(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = {}


class ChatRequest(BaseModel):
    query: str
    user_profile: Dict[str, Any] = {}  # 城市/期望薪资/技能/经验等
    top_k: int = 6
    filters: Dict[str, Any] = {}  # Chroma metadata filters

#
# - /ingest：Job/FAQ/面经等导入。生产可做增量 + 去重 + 清洗。
@app.post("/ingest")
def ingest(items: List[IngestItem]):
    text = [i.text for i in items]
    metadata = [i.metadata for i in items]
    ids = [i.id for i in items]
    Chroma(
        collection_name="jobs_corpus",
        embedding_function=emb,
        persist_directory=CHROMA_DIR
    ).add_texts(texts=text, metadatas=metadata, ids=ids)
    vectordb.persist()
    return {"ok": True, "count": len(items)}

# 检索 → 组织 prompt → DeepSeek 生成。
@app.post("/chat")
def chat(req: ChatRequest):
    # meta data file ,eg:city/salary/skills
    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": req.top_k,
            "filter": req.filters or {}
        }
    )
    docs = retriever.get_relevant_documents(req.query)
    context = "\n\n".join([
        f"[{d.metadata.get('type', 'doc')}] id = {d.metadata.get('job_id') or d.metadata.get('job_id')} | {d.page_content[:800]} "
        for d in docs])
    system_text = """你是求职助手。使用给定的“检索上下文”回答问题。
    - 若需要，可输出一个可执行的工具调用 JSON（字段：tool_name, args），但要先基于上下文解释你的思路。
    - 注意：岗位匹配时给出理由（技能/城市/薪资/经验），并提供后续动作建议（投递/预约面试/查看详情链接）。
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system + "\n\n[检索上下文]:\n{context}\n\n[用户画像]:\n{profile}"),
        ("human", "{question}")
    ])

    messages = prompt.format_messages(
        context=context,
        profile=req.user_profile,
        question=req.query
    )
    resp = llm[messages]

    return {
        "answer": resp.content,
        "chunks": [
            {"metadata": d.metadata, "snippet": d.page_content[:300]} for d in docs
        ]
    }
