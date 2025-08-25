import re

def clean_text_for_llm(text: str) -> str:
    """LLM処理用にテキストをクリーンアップ"""
    try:
        # 制御文字を除去
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # 特殊な数式記号を読みやすい形に変換
        text = re.sub(r'([a-zA-Z])([₀-₉]+)', r'\1_\2', text)  # 下付き文字
        text = re.sub(r'([a-zA-Z])([⁰-⁹]+)', r'\1^\2', text)  # 上付き文字
        
        # 波括弧を除去または置換（数式でよく使われるため）
        text = text.replace('{', '(')
        text = text.replace('}', ')')
        
        # 連続する空白を単一の空白に
        text = re.sub(r'\s+', ' ', text)
        
        # 前後の空白を除去
        text = text.strip()
        
        return text
        
    except Exception as e:
        # クリーンアップに失敗した場合は元のテキストを返す
        print(f"Text cleaning failed: {e}")
        return text