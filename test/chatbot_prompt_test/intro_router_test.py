import json
from lifewatch.llm.llm_classify.utils import create_ChatTongyiModel
from lifewatch.llm.custom_prompt.chatbot_prompt.feature_introduce import intro_router_template
from lifewatch.llm.llm_classify.schemas.user_guide_schemas import GuideSection,UserGuide,SummaryOption
from lifewatch.llm.llm_classify.utils.user_guide_parser import load_user_guide
chat_model = create_ChatTongyiModel(enable_search=False,
                            enable_thinking=False,
                            enable_streaming=False,temperature=0.5)
option = SummaryOption(id = True,title = False,abstract = True)
guide = load_user_guide()
question = "可以多设备同步吗？"
# 初始化 usage 统计
usage = {
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0,
    "call_count": 0
}

def update_usage(result):
    """从 result 中提取并累加 token 使用量"""
    token_usage = result.response_metadata.get("token_usage", {})
    usage["input_tokens"] += token_usage.get("input_tokens", 0)
    usage["output_tokens"] += token_usage.get("output_tokens", 0)
    usage["total_tokens"] += token_usage.get("total_tokens", 0)
    usage["call_count"] += 1

def test_for_intro_router():
    """两次路由版本：先粗筛再细筛"""
    from lifewatch.llm.custom_prompt.chatbot_prompt.feature_introduce import intro_template
    
    # 重置 usage 统计
    usage["input_tokens"] = 0       
    usage["output_tokens"] = 0       
    usage["total_tokens"] = 0       
    usage["call_count"] = 0
    
    all_ids = guide.get_all_ids()
    
    # 第一次调用：粗筛
    print("=== 第1步：粗筛路由 ===")
    outline = guide.transform_to_table(guide.get_children_summary(options=option))
    result = chat_model.invoke(intro_router_template.format(outline=outline, question=question))
    update_usage(result)
    id_list = json.loads(result.content)
    print(f"路由结果: {id_list}")
    
    # 获取新的outline
    outline = []
    for id in id_list:
        if id not in all_ids:
            raise ValueError(f"Invalid section ID: {id}")   
        else:
            outline += guide.get_children_summary(id, options=option)
    
    # 第二次调用：细筛
    print("\n=== 第2步：细筛路由 ===")
    outline = guide.transform_to_table(outline)
    print(f"细筛范围:\n{outline}")
    result = chat_model.invoke(intro_router_template.format(outline=outline, question=question))
    update_usage(result)
    id_list = json.loads(result.content)
    print(f"路由结果: {id_list}")

    # 获取content
    print("\n=== 第3步：获取内容 ===")
    content = ""
    for id in id_list:
        if id not in all_ids:
            raise ValueError(f"Invalid section ID: {id}")   
        else:
            content += guide.get_section_as_markdown(id,start_level=3,max_heading_depth=3)
            content += "\n"
    print(f"获取的内容:\n{content}")

    # 第三次调用：生成功能介绍
    print("\n=== 第4步：生成功能介绍 ===")
    result = chat_model.invoke(intro_template.format(guide_content=content, question=question))
    update_usage(result)
    print(f"功能介绍结果:\n{result.content}")

    # 打印 usage 统计
    print("\n=== Token Usage 统计 ===")
    print(f"调用次数: {usage['call_count']}")
    print(f"输入 Tokens: {usage['input_tokens']}")
    print(f"输出 Tokens: {usage['output_tokens']}")
    print(f"总 Tokens: {usage['total_tokens']}")


def test_for_intro_router_for_once():
    """简化版本：只进行一次路由调用后直接获取内容并生成回复"""
    from lifewatch.llm.custom_prompt.chatbot_prompt.feature_introduce import intro_template
    
    # 重置 usage 统计
    usage["input_tokens"] = 0
    usage["output_tokens"] = 0
    usage["total_tokens"] = 0
    usage["call_count"] = 0
    
    # 第一次调用：路由选择
    outline = guide.transform_to_table(guide.get_children_summary(options=option))
    result = chat_model.invoke(intro_router_template.format(outline=outline, question=question))
    update_usage(result)
    print("=== 路由结果 ===")
    print(result.content)
    
    # 将 JSON 字符串解析为列表
    id_list = json.loads(result.content)
    all_ids = guide.get_all_ids()
    
    # 直接获取 content（跳过第二次路由筛选）
    content = ""
    for id in id_list:
        if id not in all_ids:
            raise ValueError(f"Invalid section ID: {id}")   
        else:
            content += guide.get_section_as_markdown(id,start_level=3,max_heading_depth=3)
            content += "\n"
    print("\n=== 获取的内容 ===")
    print(content)
    
    # 第二次调用：生成功能介绍
    result = chat_model.invoke(intro_template.format(guide_content=content, question=question))
    update_usage(result)
    print("\n=== 功能介绍结果 ===")
    print(result.content)
    
    # 打印 usage 统计
    print("\n=== Token Usage 统计 ===")
    print(f"调用次数: {usage['call_count']}")
    print(f"输入 Tokens: {usage['input_tokens']}")
    print(f"输出 Tokens: {usage['output_tokens']}")
    print(f"总 Tokens: {usage['total_tokens']}")


if __name__ == "__main__":
    print("=" * 50)
    print("测试一次路由版本")
    print("=" * 50)
    test_for_intro_router_for_once()
    print("=" * 50)
    print("测试两次路由版本")
    print("=" * 50)
    test_for_intro_router()
    # 测试结果，第二张应该更好