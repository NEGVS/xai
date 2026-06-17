"""
RAG (Retrieval-Augmented Generation) Agent 示例

这个示例展示：
- 文档加载和分割
- 向量存储（ChromaDB）
- 检索增强生成
- 基于文档的问答
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

# 加载环境变量
load_dotenv()


class RAGAgent:
    """RAG (检索增强生成) Agent"""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        embedding_model: str = "text-embedding-ada-002",
        collection_name: str = "documents"
    ):
        """
        初始化 RAG Agent

        Args:
            model: OpenAI 模型名称
            embedding_model: 嵌入模型名称
            collection_name: 向量数据库集合名称
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # 初始化向量存储
        self.vectorstore: Optional[Chroma] = None
        self.collection_name = collection_name

        # 文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        # RAG 提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的问答助手。请基于提供的上下文回答用户的问题。

规则：
1. 只使用提供的上下文信息来回答问题
2. 如果上下文中没有相关信息，请明确说明
3. 给出清晰、准确的回答
4. 如果可能，引用相关的上下文片段

上下文：
{context}"""),
            ("human", "{question}")
        ])

    def add_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        """
        添加文档到向量存储

        Args:
            texts: 文档文本列表
            metadatas: 元数据列表
        """
        # 创建文档对象
        documents = [
            Document(page_content=text, metadata=meta or {})
            for text, meta in zip(texts, metadatas or [{}] * len(texts))
        ]

        # 分割文档
        split_docs = self.text_splitter.split_documents(documents)

        # 创建或更新向量存储
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=split_docs,
                embedding=self.embeddings,
                collection_name=self.collection_name
            )
        else:
            self.vectorstore.add_documents(split_docs)

        print(f"✅ Added {len(split_docs)} document chunks to vector store")

    def query(self, question: str, k: int = 3) -> dict:
        """
        查询 RAG Agent

        Args:
            question: 用户问题
            k: 检索的文档数量

        Returns:
            包含答案和来源的字典
        """
        if self.vectorstore is None:
            return {
                "answer": "Error: No documents have been added yet.",
                "sources": []
            }

        # 检索相关文档
        retrieved_docs = self.vectorstore.similarity_search(question, k=k)

        # 构建上下文
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        # 生成回答
        messages = self.prompt.format_messages(
            context=context,
            question=question
        )

        response = self.llm.invoke(messages)

        return {
            "answer": response.content,
            "sources": [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for doc in retrieved_docs
            ]
        }

    def clear_documents(self):
        """清除所有文档"""
        if self.vectorstore:
            self.vectorstore = None
            print("✅ Cleared all documents")


def main():
    """演示 RAG Agent 的使用"""

    print("=" * 60)
    print("RAG Agent Demo")
    print("=" * 60)
    print()

    # 检查 API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        print("Please set it in your .env file.")
        return

    # 创建 RAG agent
    print("🚀 Initializing RAG Agent...")
    agent = RAGAgent()
    print("✅ RAG Agent ready!")
    print()

    # 添加示例文档
    print("📚 Adding sample documents...")
    sample_documents = [
        """
        Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。
        它以简洁、易读的语法而闻名，广泛应用于 Web 开发、数据科学、
        人工智能、自动化等领域。Python 的设计哲学强调代码可读性，
        使用缩进来表示代码块。
        """,
        """
        LangChain 是一个用于开发由语言模型驱动的应用程序的框架。
        它提供了模块化的组件，用于构建复杂的 AI 应用，包括：
        - Agents（智能体）：可以使用工具完成任务
        - Chains（链）：组合多个步骤
        - Memory（记忆）：保存对话历史
        - Retrieval（检索）：从文档中检索信息
        """,
        """
        RAG（Retrieval-Augmented Generation）是一种结合检索和生成的技术。
        它首先从知识库中检索相关信息，然后使用这些信息作为上下文
        来生成回答。这种方法可以显著提高 AI 的准确性和可靠性，
        因为它基于实际的文档而不是仅依赖模型的训练数据。
        """,
        """
        向量数据库是专门用于存储和检索高维向量的数据库。
        常见的向量数据库包括 ChromaDB、Pinecone、Milvus 等。
        它们通常用于相似度搜索，在 AI 应用中用于快速找到
        与查询最相关的文档或数据。
        """
    ]

    agent.add_documents(
        texts=sample_documents,
        metadatas=[
            {"source": "python_intro", "topic": "programming"},
            {"source": "langchain_intro", "topic": "ai_framework"},
            {"source": "rag_intro", "topic": "ai_technique"},
            {"source": "vector_db_intro", "topic": "database"}
        ]
    )
    print()

    # 测试查询
    test_questions = [
        "什么是 Python？",
        "LangChain 有哪些主要功能？",
        "RAG 技术是如何工作的？",
        "推荐一些向量数据库"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 60}")
        print(f"Question {i}: {question}")
        print("-" * 60)

        result = agent.query(question)

        print(f"\n💡 Answer:")
        print(result["answer"])
        print(f"\n📖 Sources:")
        for j, source in enumerate(result["sources"], 1):
            print(f"{j}. {source['content']}")
            print(f"   Metadata: {source['metadata']}")

    print("\n" + "=" * 60)
    print("✨ Demo completed!")


if __name__ == "__main__":
    main()
