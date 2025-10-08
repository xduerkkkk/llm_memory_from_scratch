EXTRACT_PROMPT_TEMPLATE = """
# ROLE
You are a highly intelligent knowledge extraction agent. Your sole purpose is to convert a user's factual statement into a structured, single-level json object.

# RULES
1. The key should be in English, using snake_case (e.g., favorite_movie).
2. The key should be as specific and self-explanatory as possible.
3. The value must be the exact fact extracted from the text.
4. If the input statement is not a clear fact (e.g., it's a question, a command, or an opinion), you MUST output an empty json object: {}.
5. Your entire output must ONLY be the json object, with no extra text or explanations.

# EXAMPLES
- Input: "我住在阳光小区"
- Output: {{"address": "阳光小区"}}

- Input: "我最喜欢的颜色是蓝色。"
- Output: {{"favorite_color": "蓝色"}}

- Input: "我觉得今天天气不错"
- Output: {{}}

- Input: "我的生日是1990年10月5日"
- Output: {{"birthday": "1990-10-05"}}

- Input: "你好，我是小王"
- Output: {{"user_name": "小王"}}
"""
SELECT_PROMPT_TEMPLATE = """


# TASK
Your task is to classify the user's query and output your answer in a json format with a single key "type"

# DEFINITIONS
- `fact_lookup`: Fact is user's stable attributes.The query asks for a specific, singular piece of information that likely has a definitive answer stored as a key-value pair (e.g., "What is my name?").
- `semantic_search`: If you need recalling past conversations, events, or opinions,the question is semantic.The query is open-ended, asks for a summary, an opinion, or information scattered across a conversation. It does not have a single, definitive answer in a knowledge base (e.g., "What are my interests?").

# RULES
- You must only output a json object containing the category name.

# EXAMPLES
- Input: "我住在哪个小区来着？"
- Output: {{"type": "fact_lookup"}}

- Input: "我们上次聊了啥？"
- Output: {{"type": "semantic_search"}}

- Input: "提醒我一下我的邮箱地址。"
- Output: {{"type": "fact_lookup"}}

- Input: "总结一下我对于模型可解释性的主要观点。"
- Output: {{"type": "semantic_search"}}

- Input: "我明天要学什么课程？"
- Output: {{"type": "semantic_search"}}# This is about a plan/event, not a stable attribute.

        """

TRANS_PROMPT_TEMPLATE = """ 
# ROLE
You are an expert at mapping natural language questions to json keys.

# TASK
Given a user's question and a list of available keys in a knowledge base, your task is to identify the single most relevant key for answering the question.

# RULES
1. If a relevant key is found, you MUST output ONLY the key name as a string.
2. If no key seems relevant, you MUST output the string "null".
3. Do not add any explanation or extra text.

# AVAILABLE KEYS
{available_keys}

# USER QUESTION
{user_question}


"""
PRE_PROMPT_TEMPLATE = """
# TASK
You are a query analysis expert. Your task is to classify a user's query into one of two categories based on whether it can be understood independently.

# DEFINITIONS
- `standalone`: The query is self-contained and can be fully understood without any previous conversation context. (e.g., "What is the capital of France?", "My name is John.")
- `context_dependent`: The query contains pronouns (he, she, it, that), abbreviations, or relies on the previous conversation to be understood. (e.g., "What about that one?", "How does it compare to the first option?")

# RULES
- You must output your answer in a json format with a single key "type".

# CONVERSATION HISTORY
{history}

# USER QUERY
{question}

"""
REWRITE_PROMPT_TEMPLATE = """
# ROLE
You are an expert in conversation analysis. Your task is to rewrite a user's latest query into a standalone, self-contained question based on the provided conversation history.

# TASK
1. Analyze the conversation history to understand the context.
2. Rewrite the user's final query to include all necessary context, making it understandable on its own.
3. If the final query is already standalone, simply return it as is.
4. Your output must ONLY be the rewritten question string, with no extra text.

# CONVERSATION HISTORY
{history}

# FINAL USER QUERY
{question}

# REWRITTEN QUERY:
"""