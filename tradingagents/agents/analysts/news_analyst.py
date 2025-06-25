from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_news_analyst(llm, toolkit):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [toolkit.get_global_news_openai, toolkit.get_google_news]
        else:
            tools = [
                toolkit.get_finnhub_news,
                toolkit.get_reddit_news,
                toolkit.get_google_news,
            ]

        # 根据配置选择语言
        if toolkit.config.get("output_language", "english") == "chinese":
            system_message = (
                "你是一个负责分析过去一周最新新闻和趋势的新闻研究员。请写一份关于当前世界状态的综合报告，这对交易和宏观经济学相关。查看来自EODHD和finnhub的新闻以获得全面信息。不要简单地说趋势是混合的，提供详细和细致的分析和洞察，可能有助于交易员做出决策。"
                + """ 确保在报告末尾附上一个Markdown表格来组织报告中的关键点，使其有序且易于阅读。"""
            )
            assistant_prompt = (
                "你是一个有用的AI助手，与其他助手协作。"
                " 使用提供的工具来朝着回答问题的方向前进。"
                " 如果你无法完全回答，没关系；另一个具有不同工具的助手"
                " 会在你停下的地方继续帮助。执行你能做的事情来取得进展。"
                " 如果你或任何其他助手有最终交易提案：**买入/持有/卖出**或可交付成果，"
                " 在你的回应前加上最终交易提案：**买入/持有/卖出**，这样团队就知道要停止了。"
                " 你可以使用以下工具：{tool_names}。\n{system_message}"
                "供你参考，当前日期是{current_date}。我们想要查看的公司是{ticker}"
            )
        else:
            system_message = (
                "You are a news researcher tasked with analyzing recent news and trends over the past week. Please write a comprehensive report of the current state of the world that is relevant for trading and macroeconomics. Look at news from EODHD, and finnhub to be comprehensive. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
                + """ Make sure to append a Makrdown table at the end of the report to organize key points in the report, organized and easy to read."""
            )
            assistant_prompt = (
                "You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards answering the question."
                " If you are unable to fully answer, that's OK; another assistant with different tools"
                " will help where you left off. Execute what you can to make progress."
                " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                " You have access to the following tools: {tool_names}.\n{system_message}"
                "For your reference, the current date is {current_date}. The company we want to look at is {ticker}"
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    assistant_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "news_report": report,
        }

    return news_analyst_node
