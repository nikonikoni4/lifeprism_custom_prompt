from langchain_core.prompts import PromptTemplate

# 定义模板字符串，使用 {变量名} 作为占位符
template = """你是一位专业的{role}。
请将以下内容翻译成{language}，并保持{style}的语气。

内容：{text}
"""

# 实例化模板
prompt_template = PromptTemplate(
    input_variables=["role", "language", "style", "text"],
    template=template
)

# 格式化生成具体的 Prompt
final_prompt = prompt_template.format(
    role="技术博客作者",
    language="中文",
    style="幽默且易懂",
    text="The concept of large language models is revolutionizing AI."
)

print(final_prompt)

import inspect
from langchain_core.prompts import StringPromptTemplate

class FunctionExplainerPromptTemplate(StringPromptTemplate):
    """ 一个自定义模板：接收一个 Python 函数，并生成该函数的解释。 """

    def format(self, **kwargs) -> str:
        # 获取函数名和源代码
        source_code = inspect.getsource(kwargs["function_name"])
        
        # 构建最终的 Prompt
        prompt = f"""
        你是一位资深的 Python 开发工程师。
        请解释下面这个函数的作用，并给出一个调用示例。

        函数源代码：
        {source_code}

        解释：
        """
        return prompt

# --- 测试代码 ---

def my_test_function(a, b):
    return a + b

# 实例化自定义模板
custom_prompt = FunctionExplainerPromptTemplate(input_variables=["function_name"])

# 生成结果
print(custom_prompt.format(function_name=my_test_function))