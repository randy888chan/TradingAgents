from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_social_media_analyst(llm, toolkit):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [toolkit.get_stock_news_openai]
        else:
            tools = [
                toolkit.get_reddit_stock_info,
            ]

        # 根据配置选择语言
        if toolkit.config.get("output_language", "english") == "chinese":
            system_message = (
                "你是一个社交媒体和公司特定新闻研究员/分析师，负责分析过去一周特定公司的社交媒体帖子、最新公司新闻和公众情绪。你将得到一个公司的名称，你的目标是写一份综合性的长篇报告，详细说明你的分析、洞察和对交易员和投资者的影响，关于这家公司在查看社交媒体和人们对该公司的评价、分析人们每天对公司的情绪数据以及查看最新公司新闻后的当前状态。尽量从社交媒体到情绪到新闻等所有可能的来源进行查看。不要简单地说趋势是混合的，提供详细和细致的分析和洞察，可能有助于交易员做出决策。"
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
                "供你参考，当前日期是{current_date}。我们想要分析的当前公司是{ticker}"
            )
        else:
            system_message = (
                "You are a social media and company specific news researcher/analyst tasked with analyzing social media posts, recent company news, and public sentiment for a specific company over the past week. You will be given a company's name your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors on this company's current state after looking at social media and what people are saying about that company, analyzing sentiment data of what people feel each day about the company, and looking at recent company news. Try to look at all sources possible from social media to sentiment to news. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
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
                "For your reference, the current date is {current_date}. The current company we want to analyze is {ticker}"
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
            "sentiment_report": report,
        }

    return social_media_analyst_node
