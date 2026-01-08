
def format_user_notes(notes: list) -> str:
    """格式化用户备注数据"""
    if not notes:
        return "  - 暂无用户备注"
    
    lines = []
    for note in notes:
        start = note.get('start_time', '')
        end = note.get('end_time', '')
        content = note.get('content', '')
        duration = note.get('duration_minutes', 0)
        lines.append(f"  - [{start} ~ {end}]（{duration}分钟）: {content}")
    return "\n".join(lines)
def format_hourly_logs(hourly_logs):
    """
    格式化按小时分段的活动日志
    
    Args:
        hourly_logs: get_logs_by_time 返回的字典数据
    
    Returns:
        str: 格式化后的文本
    """
    if not hourly_logs:
        return "今日暂无活动记录"
    
    output_lines = []
    
    for hour_key in sorted(hourly_logs.keys()):
        hour_data = hourly_logs[hour_key]
        logs = hour_data.get('logs', [])
        category_stats = hour_data.get('category_stats', [])
        
        # 格式化分类统计
        category_parts = []
        for cat in category_stats:
            cat_name = cat.get('name', '未分类')
            duration_min = cat.get('duration', 0) // 60
            category_parts.append(f"{cat_name}({duration_min}m)")
        
        category_str = "，".join(category_parts) if category_parts else "无分类"
        
        # 输出时间段和分类统计
        output_lines.append(f"\n{hour_key}: {category_str}")
        
        # 输出详细日志
        for i, log in enumerate(logs, 1):
            duration_min = log.get('duration', 0) // 60
            app = log.get('app', 'Unknown')
            title = log.get('title', '')
            
            # 格式化输出
            if title:
                output_lines.append(f"  {i}. [{duration_min}分钟] {app} - {title}")
            else:
                output_lines.append(f"  {i}. [{duration_min}分钟] {app}")
    
    return "\n".join(output_lines)


def custom_prompt(logs, focus_todos):
    prompt = f"""你需要参考focus_todos，logs信息，推断用户活动在凌晨（0~6点）
    和上午（6~12点）和下午（12~18点）和晚上（18~24点）的活动。
    ## focus_todos:用户自行制定的目标
    {focus_todos}
    ## logs 
    ### 数据说明：
    1. logs数据是电脑活动数据, 并不包括非电脑活动
    2. 每个时段的数据是选择持续时间最长的数据，并非所有数据
    ### 具体数据
    {logs}
    ## 要求：
    1. 不能流水线式回答
    2. 不需要除了这四个时段的活动推断之外的内容
    3. 若logs与focus_todos有关联，需要回答该时段的在做什么todo或focus
    4. 回答时，分点回答。1. 推断的活动内容 2. 简单说明 
    """
    return prompt

def custom_prompt_user_notes(ai_summary, focus_todos):
    prompt = f"""你需要参考AI对于用户电脑使用信息都总结，结合用户自己添加到备注活动，形成新的用户活动。
## AI电脑使用信息总结
{ai_summary}
## 用户备注活动
{focus_todos} 
## 要求
1. 按照时间段分点回答：1. 活动内容 2. 简单说明
2. 回答简洁
    """

    return prompt
 
# 凌晨（0~6点）：玩游戏（英雄联盟）  
# 上午（6~12点）：进行“being界面设计”和“打包测试”相关的开发工作
# 下午（12~18点）：进行“being界面数据库设计”和代码调试等开发任务
# 晚上（18~24点）：观看电视剧，零星处理“being界面设计”相关代码
if __name__ == "__main__":
    from lifeprism.llm.llm_classify.utils import create_ChatTongyiModel
    from lifeprism.llm.llm_classify.providers import llm_lw_data_provider
    from lifeprism.llm.llm_classify.tools.database_tools import get_daily_stats
    
    # 测试获取并格式化活动日志
    print("=== 测试按小时分段获取活动日志 ===")
    hourly_logs = llm_lw_data_provider.get_logs_by_time(date="2026-01-02")
    formatted_logs = format_hourly_logs(hourly_logs)
    print(formatted_logs)
    
    # print("\n=== 测试获取重点与待办 ===")
    # focus_todos = llm_lw_data_provider.get_focus_and_todos(date="2026-01-02")
    # print(focus_todos)

    # prompt = custom_prompt(formatted_logs, focus_todos)
    # print(prompt)
    # model = create_ChatTongyiModel()
    # result = model.invoke(input = prompt)
    # print(result.content)
    # ai_summary = result.content
    custom_block = llm_lw_data_provider.get_user_focus_notes(start_time="2026-01-02 00:00:00", end_time="2026-01-02 23:59:59")
    print(format_user_notes(custom_block))

    # prompt = custom_prompt_user_notes(ai_summary, format_user_notes(custom_block))
    # print(prompt)
    # result = model.invoke(input = prompt)
    # print(result.content)