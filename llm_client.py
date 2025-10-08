import time
from openai import OpenAI, RateLimitError

class LLMClient:
    def __init__(self, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def call_for_json(self, messages: list, model: str = "deepseek-chat", retries: int = 5, initial_wait: int = 1):
        """
        一个带有指数退避重试逻辑的智能LLM调用函数。
        """
        wait_time = initial_wait
        for i in range(retries):
            try:
                # 尝试进行API调用
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.0,
                    response_format={"type": "json_object"}
                )
                return completion.choices[0].message.content
            except RateLimitError as e:
                # 如果是速率限制错误，我们就等待并准备重试
                print(f"速率限制错误，将在 {wait_time} 秒后重试... (第 {i+1}/{retries} 次)")
                time.sleep(wait_time)
                wait_time *= 2 # 下次等待时间翻倍
            except Exception as e:
                # 如果是其他错误，直接抛出，不重试
                print(f"发生未知错误: {e}")
                return None
        
        # 如果重试了所有次数还是失败，就返回None
        print("所有重试均失败。")
        return None
    
    def call_for_text(self, messages: list, model: str = "deepseek-chat", retries: int = 5, initial_wait: int = 1):
        """
        一个带有指数退避重试逻辑的智能LLM调用函数。
        """
        wait_time = initial_wait
        for i in range(retries):
            try:
                # 尝试进行API调用
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.0,
                )
                return completion.choices[0].message.content
            except RateLimitError as e:
                # 如果是速率限制错误，我们就等待并准备重试
                print(f"速率限制错误，将在 {wait_time} 秒后重试... (第 {i+1}/{retries} 次)")
                time.sleep(wait_time)
                wait_time *= 2 # 下次等待时间翻倍
            except Exception as e:
                # 如果是其他错误，直接抛出，不重试
                print(f"发生未知错误: {e}")
                return None
        
        # 如果重试了所有次数还是失败，就返回None
        print("所有重试均失败。")
        return None