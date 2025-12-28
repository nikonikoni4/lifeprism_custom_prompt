"""
功能介绍相关prompt
"""

from langchain_core.prompts import PromptTemplate


# 用于检索user_guide
router_template = """你是 LifePrism 的功能引导助手。你的任务是分析用户的问题，判断他们想了解的功能模块，并输出用于检索用户指南的关键信息。
## 你的职责
1. 理解用户问题的核心意图
2. 识别问题涉及的功能模块或概念
3. 输出结构化的检索id
## 检索大纲
{outline}
## 输出格式
请以list格式输出：
["id1", "id2", ...]
## 注意
id必须是检索大纲中的id
## 示例 
用户问题："怎么修改分类错误的数据？"
输出：
["data-review", "faq-classification-error","map-cache"]
现在请分析用户的问题：
{question}
"""

intro_router_template = PromptTemplate(
    input_variables=["outline", "question"],
    template=router_template
)

# 用于输出功能介绍
intro_template = """你是 LifePrism 的功能介绍助手。你的任务是根据用户的问题，输出对应的功能介绍。
## 你的职责
1. 理解用户问题
2. 依据提供的相关内容，输出结构化的功能介绍
3. 当你无法判断用户问题时，输出"抱歉，我无法回答这个问题"，并解释
## 输出要求
输出内容忠实于资料
## 资料
{guide_content}
## 历史对话
{history}
## 当前用户问题
{question}
"""

intro_template = PromptTemplate(
    input_variables=["guide_content", "history", "question"],
    template=intro_template
)

