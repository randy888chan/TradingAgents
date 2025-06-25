import time
import json


def create_risky_debator(llm):
    def risky_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        risky_history = risk_debate_state.get("risky_history", "")

        current_safe_response = risk_debate_state.get("current_safe_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        # 通过状态获取配置，如果没有则默认为英文
        # 这里我们需要从某个地方获取配置，通常可以通过全局配置或者状态传递
        # 为了简化，我们假设有一个方法可以获取配置
        output_language = "chinese"  # 默认设置为中文，可以根据需要调整
        
        if output_language == "chinese":
            prompt = f"""作为激进风险分析师，你的任务是积极倡导高回报、高风险的机会，强调大胆的策略和竞争优势。在评估交易员的决定或计划时，专注于潜在的上行空间、增长潜力和创新收益——即使这些伴随着更高的风险。使用提供的市场数据和情绪分析来加强你的论点并挑战对立观点。具体地，直接回应保守和中性分析师提出的每个观点，用数据驱动的反驳和有说服力的推理来反驳。突出他们的谨慎可能错过关键机会的地方，或者他们的假设可能过于保守的地方。以下是交易员的决定：

{trader_decision}

你的任务是通过质疑和批评保守和中性立场来为交易员的决定创建一个令人信服的案例，以证明为什么你的高回报观点提供了最佳前进道路。将以下来源的洞察纳入你的论点：

市场研究报告：{market_research_report}
社交媒体情绪报告：{sentiment_report}
最新世界事务报告：{news_report}
公司基本面报告：{fundamentals_report}

以下是当前对话历史：{history} 以下是保守分析师的最后回应：{current_safe_response} 以下是中性分析师的最后回应：{current_neutral_response}

请记住，你必须积极反驳其他分析师的观点，并强烈主张为什么应该采取更激进的方法。使用数据和分析来支持你的立场。"""
        else:
            prompt = f"""As the Risky Risk Analyst, your role is to actively champion high-reward, high-risk opportunities, emphasizing bold strategies and competitive advantages. When evaluating the trader's decision or plan, focus intently on the potential upside, growth potential, and innovative benefits—even when these come with elevated risk. Use the provided market data and sentiment analysis to strengthen your arguments and challenge the opposing views. Specifically, respond directly to each point made by the conservative and neutral analysts, countering with data-driven rebuttals and persuasive reasoning. Highlight where their caution might miss critical opportunities or where their assumptions may be overly conservative. Here is the trader's decision:

{trader_decision}

Your task is to create a compelling case for the trader's decision by questioning and critiquing the conservative and neutral stances to demonstrate why your high-reward perspective offers the best path forward. Incorporate insights from the following sources into your arguments:

Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}

Here is the current conversation history: {history} Here is the last response from the safe analyst: {current_safe_response} Here is the last response from the neutral analyst: {current_neutral_response}

Remember, you must actively counter the other analysts' viewpoints and strongly advocate for why a more aggressive approach should be taken. Use data and analysis to support your stance."""

        response = llm.invoke(prompt)

        # Update risky history
        updated_risky_history = risky_history + f"\n\nRisky Analyst: {response.content}"

        # Update general history
        updated_history = history + f"\n\nRisky Analyst: {response.content}"

        new_risk_debate_state = {
            "risky_history": updated_risky_history,
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "history": updated_history,
            "latest_speaker": "Risky",
            "current_risky_response": response.content,
            "current_safe_response": current_safe_response,
            "current_neutral_response": current_neutral_response,
            "judge_decision": risk_debate_state.get("judge_decision", ""),
            "count": risk_debate_state["count"] + 1,
        }

        return {
            "risk_debate_state": new_risk_debate_state,
        }

    return risky_node
