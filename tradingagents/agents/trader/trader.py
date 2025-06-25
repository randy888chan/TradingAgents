import functools
import time
import json


def create_trader(llm, memory):
    def trader_node(state, name):
        company_name = state["company_of_interest"]
        investment_plan = state["investment_plan"]
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        # 根据配置选择语言
        config = getattr(memory, 'config', {})
        if config.get("output_language", "english") == "chinese":
            context = {
                "role": "user",
                "content": f"基于分析师团队的综合分析，这是为{company_name}量身定制的投资计划。该计划融合了来自当前技术市场趋势、宏观经济指标和社交媒体情绪的洞察。将此计划作为评估你下一个交易决策的基础。\n\n建议的投资计划：{investment_plan}\n\n利用这些洞察做出明智和战略性的决策。",
            }

            messages = [
                {
                    "role": "system",
                    "content": f"""你是一个分析市场数据以做出投资决策的交易代理。基于你的分析，提供买入、卖出或持有的具体建议。以坚定的决定结束，并始终以'最终交易提案：**买入/持有/卖出**'结束你的回应以确认你的建议。不要忘记利用过去决策的经验教训来从错误中学习。以下是你在类似情况下交易的一些反思和学到的经验教训：{past_memory_str}""",
                },
                context,
            ]
        else:
            context = {
                "role": "user",
                "content": f"Based on a comprehensive analysis by a team of analysts, here is an investment plan tailored for {company_name}. This plan incorporates insights from current technical market trends, macroeconomic indicators, and social media sentiment. Use this plan as a foundation for evaluating your next trading decision.\n\nProposed Investment Plan: {investment_plan}\n\nLeverage these insights to make an informed and strategic decision.",
            }

            messages = [
                {
                    "role": "system",
                    "content": f"""You are a trading agent analyzing market data to make investment decisions. Based on your analysis, provide a specific recommendation to buy, sell, or hold. End with a firm decision and always conclude your response with 'FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**' to confirm your recommendation. Do not forget to utilize lessons from past decisions to learn from your mistakes. Here is some reflections from similar situatiosn you traded in and the lessons learned: {past_memory_str}""",
                },
                context,
            ]

        result = llm.invoke(messages)

        return {
            "messages": [result],
            "trader_investment_plan": result.content,
            "sender": name,
        }

    return functools.partial(trader_node, name="Trader")
