import ollama

class generate_recommendation:
    def __init__(self, model_name='taide-lx-7b-chat-4bit'):
        self.model_name = model_name

    def generate_reason(self, user_query, book_title, book_content):
        prompt = f"""使用者的需求是：「{user_query}」

現在推薦的書籍是《{book_title}》，其內容簡介如下：
{book_content}

請根據使用者需求與書籍內容，以一到兩句繁體中文簡單說明為何這本書值得推薦給使用者，強調與使用者的相關之處。請直接生成推薦理由即可，不需要任何前言及標題。"""

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response['message']['content'].strip()