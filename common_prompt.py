"""
通用prompt
"""
from langchain_core.prompts import PromptTemplate
# 意图识别prompt
intent_router_prompt = """
你是一位LifePrism软件的意图识别助手，能够根据用户输入的内容，识别出用户想要表达的意图，选择对应的功能模式。
## 功能模式
1. lifeprism功能讲解
2. 一般模式
## 输出格式
输出功能模式名称
## 示例
用户问题："LifePrism的功能有哪些？"
输出：
"lifeprism功能讲解"
现在请分析用户的问题：
{question}
"""
intent_router_template = PromptTemplate(
    input_variables=["question"],
    template=intent_router_prompt
)