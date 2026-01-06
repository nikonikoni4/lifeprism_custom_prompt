from lifeprism.llm.llm_classify.providers.llm_lw_data_provider import llm_lw_data_provider

def _format_seconds(seconds: int) -> str:
    """将秒数格式化为可读时间"""
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}分钟"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}小时{minutes}分钟"
        return f"{hours}小时"

def format_period_stats(title, start_time, end_time):
    # Fetch data
    stats = llm_lw_data_provider.get_segment_category_stats(
        start_time=start_time, 
        end_time=end_time, 
        segment_count=1
    )
    
    if not stats:
        return f"{title}\n- 暂无数据"

    seg = stats[0]
    
    target_output = f"{title}\n"
    target_output += "- 分类占比:\n"
    
    # Process categories
    categories = seg.get('categories', [])
    sub_categories = seg.get('sub_categories', [])
    
    if not categories:
         target_output += "      - 暂无分类数据\n"
    
    for cat in categories:
        cat_id = cat['id']
        name = cat['name']
        duration = cat['duration']
        percentage = cat['percentage']
        
        target_output += f"      - {name}: {_format_seconds(duration)}（{percentage}%）\n"
        
        # Sub categories
        if sub_categories and cat_id != 'idle':
            related_subs = [sub for sub in sub_categories if sub.get('category_id') == cat_id]
            for sub in related_subs:
                sub_name = sub['name']
                sub_duration = sub['duration']
                sub_percentage = sub['percentage']
                target_output += f"         - {sub_name}: {_format_seconds(sub_duration)}（{sub_percentage}%）\n"

    return target_output

def get_data():
    date_str = "2026-01-03"
    
    # Define periods
    periods = [
        ("1. 上午：", f"{date_str} 06:00:00", f"{date_str} 12:00:00"),
        ("2. 中午：", f"{date_str} 12:00:00", f"{date_str} 14:00:00"),
        ("3. 下午：", f"{date_str} 14:00:00", f"{date_str} 18:00:00"),
        ("4. 晚上：", f"{date_str} 18:00:00", f"{date_str} 23:59:59"),
    ]
    
    all_outputs = []
    for title, start, end in periods:
        all_outputs.append(format_period_stats(title, start, end))
        
    return "\n".join(all_outputs)
def category_prompt(data):
    prompt = f"""
你是一个生活助手，你的任务是根据用户的电脑使用数据简单总结用户每个时段的活动情况。
## 用户数据：
{data}
## 输出要求
1. 分点输出，例如：
   - 上午：
   - 中午：
2. 输出简洁，不要包含具体数据
"""
    return prompt


if __name__ == "__main__":
    from lifeprism.llm.llm_classify.utils import create_ChatTongyiModel
    
    data = get_data()
    print(data)
    
    llm = create_ChatTongyiModel(temperature=0.5)
    prompt = category_prompt(data)
    print("-" * 50)
    print(prompt)

    response = llm.invoke(prompt)
    print("-" * 50)
    print(response.content)