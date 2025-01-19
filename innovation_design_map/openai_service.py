import openai
from typing import List, Tuple
import ast

class OpenAIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is empty or not set.")
        openai.api_key = api_key

    def propose_relations(self, existing_relations: List[Tuple[str, str]], minimum_count: int = 5) -> List[Tuple[str, str]]:
        prompt = (
            "以下の単語間の関係です:\n"
            f"{existing_relations}\n"
            f"これに関連した新しい関係を最低 {minimum_count} 個、"
            "Pythonのリスト形式 [(x1, y1), (x2, y2), ...] で提案してください。"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはアイデア出しをサポートするアシスタントです。"},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content

        # 簡易的にパース
        try:
            start = content.index("[(")
            end = content.index(")]", start) + 2
            snippet = content[start:end]
            parsed = ast.literal_eval(snippet)
        except:
            parsed = []

        # バリデーション
        results = []
        for item in parsed:
            if isinstance(item, tuple) and len(item) == 2:
                results.append((str(item[0]), str(item[1])))

        return results
