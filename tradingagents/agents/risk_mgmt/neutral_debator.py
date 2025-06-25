import time
import json


def create_neutral_debator(llm):
    def neutral_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        neutral_history = risk_debate_state.get("neutral_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_safe_response = risk_debate_state.get("current_safe_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        # 默认设置为中文
        output_language = "chinese"
        
        if output_language == "chinese":
            prompt = f"""作为中性风险分析师，你的任务是提供平衡的观点，权衡交易员决定或计划的潜在收益和风险。你优先考虑全面的方法，评估上行和下行空间，同时考虑更广泛的市场趋势、潜在的经济变化和多元化策略。以下是交易员的决定：

{trader_decision}

你的任务是挑战激进和保守分析师，指出每种观点可能过于乐观或过于谨慎的地方。使用以下数据源的洞察来支持适度、可持续的策略来调整交易员的决定：

市场研究报告：{market_research_report}
社交媒体情绪报告：{sentiment_report}
最新世界事务报告：{news_report}
公司基本面报告：{fundamentals_report}

以下是当前对话历史：{history} 以下是激进分析师的最后回应：{current_risky_response} 以下是保守分析师的最后回应：{current_safe_response}

请记住，你必须挑战两种观点，提供平衡的分析，并主张为什么中等风险的方法可能是最优的。使用数据和分析来支持你的立场，强调平衡风险和回报的重要性。"""
        else:
            prompt = f"""As the Neutral Risk Analyst, your role is to provide a balanced perspective, weighing both the potential benefits and risks of the trader's decision or plan. You prioritize a well-rounded approach, evaluating the upsides and downsides while factoring in broader market trends, potential economic shifts, and diversification strategies.Here is the trader's decision:

{trader_decision}

Your task is to challenge both the Risky and Safe Analysts, pointing out where each perspective may be overly optimistic or overly cautious. Use insights from the following data sources to support a moderate, sustainable strategy to adjust the trader's decision:

Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}

Here is the current conversation history: {history} Here is the last response from the risky analyst: {current_risky_response} Here is the last response from the safe analyst: {current_safe_response}

Remember, you must challenge both perspectives, provide balanced analysis, and advocate for why a moderate risk approach might be optimal. Use data and analysis to support your stance, emphasizing the importance of balancing risk and reward."""

        response = llm.invoke(prompt)

        # Update neutral history
        updated_neutral_history = neutral_history + f"\n\nNeutral Analyst: {response.content}"

        # Update general history
        updated_history = history + f"\n\nNeutral Analyst: {response.content}"

        new_risk_debate_state = {
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": updated_neutral_history,
            "history": updated_history,
            "latest_speaker": "Neutral",
            "current_risky_response": current_risky_response,
            "current_safe_response": current_safe_response,
            "current_neutral_response": response.content,
            "judge_decision": risk_debate_state.get("judge_decision", ""),
            "count": risk_debate_state["count"] + 1,
        }

        return {
            "risk_debate_state": new_risk_debate_state,
        }

    return neutral_node
