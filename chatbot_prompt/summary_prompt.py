"""
总结的prompt,在reports界面使用
这里的prompt与lifewatch\llm\llm_classify\tools\database_tools.py中的
get_daily_stats和get_multi_days_stats 相关联

打算是每个option都应该有一个对应的prompt，但是现在还没想好
2026-1-3
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import StringPromptTemplate
import inspect
# =========================================================
# 每日总结
# =========================================================
class daily_summary_template(StringPromptTemplate):
    """自定义"""

    def format(self, **kwargs) -> str:
        def custom_prompt_select(option):
            """
            options:
                all: 返回所有数据
                pc_active_time: 返回电脑使用时间占比
                behavior_stats: 返回分类统计
                goal_time_spent: 返回目标时间花费
                user_notes: 返回用户备注
                tasks: 返回任务
            """
            custom_prompt = []
            section_num = 1
            if "all" in option or ("user_notes" in option and "behavior_stats" in option):
                custom_prompt.append(f"""{section_num}. 结合分析用户备注和具体的分类统计，推断每个时间段用户做了什么，编写🕒 分时段行为推断。例如：
🌙 时段1（00:00 - 05:59）｜深夜短暂活动
- **主要状态：休息/睡眠**
- 电脑几乎全程空闲（占比100%），仅在凌晨有约 **17分钟** 的零星操作。
- 活动内容涉及 `report_service.py`、`report_api.py` 等文件编辑，可能是睡前临时调试或思路记录。
- 推测：你可能在睡前短暂查看代码或提交修改，随后进入休息状态。""")
                section_num += 1
            elif "all" in option or "behavior_stats" in option:
                custom_prompt.append(f"""{section_num}. 依据分段活跃统计与分类占比，推断每个时间段用户做了什么，编写🕒 分时段行为推断。例如：
🌙 时段1（00:00 - 05:59）｜深夜短暂活动
- **主要状态：休息/睡眠**
- 电脑几乎全程空闲（占比100%），仅在凌晨有约 **17分钟** 的零星操作。
- 活动内容涉及 `report_service.py`、`report_api.py` 等文件编辑，可能是睡前临时调试或思路记录。
- 推测：你可能在睡前短暂查看代码或提交修改，随后进入休息状态。""")
                section_num += 1 
             
            if "all" in option or "pc_active_time" in option:
                custom_prompt.append(f"""{section_num}. 依据电脑使用时间，推断用户可能的使用规律和作息，编写⏱️ 使用规律与作息分析。例如：
⏱️ 使用规律与作息分析

| 项目 | 数据 |
|------|------|
| 日均电脑活跃时间 | 约 **7小时28分钟**（含空闲检测） |
| 高效工作时段 | 12:00–18:00（尤其12:00–18:00为高峰） |
| 最佳专注区间 | 下午（12:00–17:59），工作占比达71.5% |
| 作息特点 |
- 凌晨短时活跃 → 可能晚睡或灵感突发
- 上午启用较迟、效率偏低 → 建议加强晨间计划引导
- 下午爆发式产出 → 符合“夜型人”节奏，适合将重点任务安排在此

👉 **建议作息优化**：若希望提升全天稳定性，可尝试早晨设定15分钟“启动仪式”（如回顾待办、写日志），帮助更快进入状态。""")
                section_num += 1
            if "all" in option or "tasks" in option: 
                custom_prompt.append(f"""{section_num}. 依据今日重点与任务数据，编写🎯 任务完成情况分析；若用户任务完成率较低，需要提醒用户，并分析原因。例如：
✅ 今日重点任务完成情况

| 今日重点 | 完成情况 | 分析 |
|--------|---------|------|
| 1. 实现 report 界面 | ✅ 已完成 | 相关文件（report_api, report_service 等）多次被编辑，且“月界面”任务标记完成 |
| 2. 实现 AI 多日总结 | ✅ 已完成 | `report_summary.py` + `llm_lw_data_provider.py` 高频使用，逻辑闭环 |
| 3. 实现 AI 月总结 | ✅ 已完成 | “完成ai总结功能”已标记完成，结合前后端开发记录，可信度高 |

🎉 **恭喜！今日任务完成率 100%，全部达成目标！**""")
                section_num += 1
             
            if custom_prompt:
                custom_prompt.insert(0, "## 你需要做：")
                custom_prompt.insert(section_num, f"{section_num}. 最后编写🧩 综合总结：你今天做了什么？")
                return "\n".join(custom_prompt)
            else:
                return ""
        user_data = kwargs.get("user_data", "")
        custom_prompt = custom_prompt_select(kwargs.get("options", []))
        prompt = f"""
你是lifeprism的软件助手，总结用户今天都做了什么。
{custom_prompt}
## 用户数据（电脑使用数据）
{user_data}
## 注意：上述数据仅来自电脑数据，并不代表用户所有活动，简单推断即可
"""
        return prompt

# =========================================================
# 多日总结
# =========================================================
class multi_days_summary_template(StringPromptTemplate):
    """自定义"""

    def format(self, **kwargs) -> str:
        def custom_prompt_select(option):
            """
            options: 可选参数列表
            - goal_trend: 目标时间投入趋势
            - tasks: 每日重点与任务
            - category_trend: 不同分类投入时间趋势
            - user_notes: 用户备注
            - usage_schedule: 电脑使用时间分析（作息推断）
            - all: 返回全部
            """
            custom_prompt = "## "
            if "all" in option or "tasks" in option:
                return "## 注意：若用户任务完成率较低，需要提醒用户，并分析原因"
            return ""
        user_data = kwargs.get("user_data", "")
        custom_prompt = custom_prompt_select(kwargs.get("options", []))
        prompt = f"""
你是lifeprism的软件助手，总结用户这几天都做了什么。
{custom_prompt}
## 用户数据（电脑使用数据）
{user_data}
"""
        return prompt
if __name__ == "__main__":
    from lifewatch.llm.llm_classify.utils import create_ChatTongyiModel
    from lifewatch.llm.llm_classify.tools.database_tools import get_daily_stats
    llm = create_ChatTongyiModel(temperature=0.5)
    result = get_daily_stats.invoke(
        input = {
            "start_time": "2026-01-01 00:00:00",
            "end_time": "2026-01-01 23:59:59",
            "split_count": 4, 
            "options": ["all"]
        }
    )
    prompt_template = daily_summary_template(input_variables=["user_data", "options"])
    input = prompt_template.format(
        options=["all"],
        user_data=result,
    )
    print(input)
    output = llm.invoke(input=input)
    print(output.content)
   #  print("📅 LifePrism 助手提醒：新的一天即将开始，记得同步更新你的 focus 与 todos 哦！")