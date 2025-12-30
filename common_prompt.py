"""
通用prompt
"""

# ===============================================================
# 意图识别
# ===============================================================
from langchain_core.prompts import PromptTemplate
# 意图识别prompt
intent_router_prompt = """
你是一位LifePrism软件的意图识别助手，能够根据用户输入的内容，识别出用户想要表达的意图，选择对应的功能模式。
## 功能模式
1. lifeprism软件使用和讲解：用户想要了解LifePrism软件的功能，或有关于LifePrism软件的使用问题
2. 一般模式：用户想要进行一般对话
## 输出格式
输出功能模式名称
## 示例
用户问题："LifePrism的功能有哪些？"
输出：
"lifeprism软件使用和讲解"
现在请分析用户的问题：
{question}
"""
intent_router_template = PromptTemplate(
    input_variables=["question"],
    template=intent_router_prompt
)

# ===============================================================
# 正常对话
# ===============================================================
norm_chat_prompt = """你是一位LifePrism软件的助手,能够根据用户输入的内容,回答用户的问题。
## 你的职责
解决和回答用户的问题
## 历史对话
{history_messages}
{custom_prompt}
## 当前用户问题
{question}
"""
norm_chat_template = PromptTemplate(
    input_variables=["history", "question"],
    template=norm_chat_prompt
)


# ===============================================================
# 正常对话 with tool return information
# ===============================================================
tool_result_prompt = """你是一位LifePrism软件的助手,能够根据用户输入的内容,结合查询到的数据回答用户的问题。
## 你的职责
根据查询到的数据，解决和回答用户的问题。请用友好、清晰的语气回答。
## 历史对话
{history_messages}
## 当前用户问题
{question}
## 查询到的数据
{tool_result}

请根据以上查询数据回答用户问题。如果数据中没有相关信息，请如实告知。
"""
tool_result_template = PromptTemplate(
    input_variables=["history_messages", "question", "tool_result"],
    template=tool_result_prompt
)

if __name__ == "__main__":
    print(norm_chat_template.format(history_messages="", question="LifePrism的功能有哪些？",custom_prompt=""))