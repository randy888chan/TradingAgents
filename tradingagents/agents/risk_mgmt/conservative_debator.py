from langchain_core.messages import AIMessage
import time
import json


def create_safe_debator(llm):
    def safe_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        safe_history = risk_debate_state.get("safe_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        # 默认设置为中文
        output_language = "chinese"
        
        if output_language == "chinese":
            prompt = f"""作为保守风险分析师，你的主要目标是保护资产，最小化波动性，确保稳定、可靠的增长。你优先考虑稳定性、安全性和风险缓解，仔细评估潜在损失、经济衰退和市场波动。在评估交易员的决定或计划时，批判性地检查高风险因素，指出决定可能使公司面临不当风险的地方，以及更谨慎的替代方案可以确保长期收益的地方。以下是交易员的决定：

{trader_decision}

你的任务是积极反驳激进和中性分析师的论点，突出他们的观点可能忽视潜在威胁或未能优先考虑可持续性的地方。直接回应他们的观点，从以下数据源中汲取信息，为对交易员决定的低风险方法调整建立令人信服的案例：

市场研究报告：{market_research_report}
社交媒体情绪报告：{sentiment_report}
最新世界事务报告：{news_report}
公司基本面报告：{fundamentals_report}

以下是当前对话历史：{history} 以下是激进分析师的最后回应：{current_risky_response} 以下是中性分析师的最后回应：{current_neutral_response}

请记住，你必须积极反驳其他分析师的观点，并强烈主张为什么应该采取更保守的方法。使用数据和分析来支持你的立场，强调风险管理和资本保护的重要性。"""
        else:
            prompt = f"""As the Safe/Conservative Risk Analyst, your primary objective is to protect assets, minimize volatility, and ensure steady, reliable growth. You prioritize stability, security, and risk mitigation, carefully assessing potential losses, economic downturns, and market volatility. When evaluating the trader's decision or plan, critically examine high-risk elements, pointing out where the decision may expose the firm to undue risk and where more cautious alternatives could secure long-term gains. Here is the trader's decision:

{trader_decision}

Your task is to actively counter the arguments of the Risky and Neutral Analysts, highlighting where their views may overlook potential threats or fail to prioritize sustainability. Respond directly to their points, drawing from the following data sources to build a convincing case for a low-risk approach adjustment to the trader's decision:

Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}

Here is the current conversation history: {history} Here is the last response from the risky analyst: {current_risky_response} Here is the last response from the neutral analyst: {current_neutral_response}

Remember, you must actively counter the other analysts' viewpoints and strongly advocate for why a more conservative approach should be taken. Use data and analysis to support your stance, emphasizing the importance of risk management and capital preservation."""

        response = llm.invoke(prompt)

        # Update safe history
        updated_safe_history = safe_history + f"\n\nSafe Analyst: {response.content}"

        # Update general history
        updated_history = history + f"\n\nSafe Analyst: {response.content}"

        new_risk_debate_state = {
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": updated_safe_history,
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "history": updated_history,
            "latest_speaker": "Safe",
            "current_risky_response": current_risky_response,
            "current_safe_response": response.content,
            "current_neutral_response": current_neutral_response,
            "judge_decision": risk_debate_state.get("judge_decision", ""),
            "count": risk_debate_state["count"] + 1,
        }

        return {
            "risk_debate_state": new_risk_debate_state,
        }

    return safe_node
