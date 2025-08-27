# 🎀✨ ChatGAL ✨🎀

> **超カワイイRAGチャットボット💕 ギャル語で質問に答えちゃうよ〜🦄**

## 💎 これなに？

ChatGALは、PDFファイルをアップロードして、その内容について**ギャル語**で教えてくれちゃう超キュートなチャットボットだよ〜✨

- 📚 **RAG（Retrieval-Augmented Generation）** でスマートに回答
- 🎯 **RAGAS評価** で性能もバッチリチェック
- 💅 **ギャル語** で楽しくおしゃべり
- 🌈 **Streamlit** でサクサク動く

## 🖼️ アプリのスクショはこんな感じ

![通常のチャット](https://github.com/user-attachments/assets/c12c5ecc-d550-4ffc-879d-7ebe7b59d356 "通常のチャットの様子")

![資料のアップロード画面](https://github.com/user-attachments/assets/ca1da81c-38dc-4831-bbc7-faf303428c91 "資料のアップロード画面")

![RAGの様子](https://github.com/user-attachments/assets/91134695-6b02-4e11-980e-030caad3fa85 "RAGの様子")

![RAGASによる性能評価ページ](https://github.com/user-attachments/assets/6d21e753-27f0-460e-ab6d-9d0d2e120425 "RAGASによる性能評価ページ")

## 🚀 できること

### 💬 チャット機能

- ギャル語でなんでも質問できちゃう💖
- アップした資料を参考に回答してくれるよ〜
- 参考にした資料も見れちゃう📚

### 📤 資料アップロード

- 複数のPDFファイルを一気にアップ可能💪
- ローカルのベクトルDBに自動で保存しちゃう✨
- ファイル情報もバッチリ管理

### 💯 性能評価

- **Context Precision**: 検索精度をチェック🎯
- **Context Recall**: 情報の網羅性をチェック📊  
- **Faithfulness**: 回答の忠実性をチェック💎
- **Answer Relevancy**: 回答の関連性をチェック🔥

## 🎯 使い方

### Step 1: Azure OpenAIのモデル設定 📚

1. **サイドバー**の「🔧 Azure OpenAI設定」からAPIを設定
2. すべて入力したら「接続テスト」ボタンをクリックして設定完了
3. リポジトリをクローンし`.env`ファイルを用意して実行する場合は「環境変数から読み込み」をクリックするだけ

### Step 2: 資料をアップ 📚

1. **資料アップ**ページに移動
2. PDFファイルを選択してアップロード
3. 処理完了まで待つ（ちょっと時間かかるかも💦）

### Step 3: チャットで質問 💬

1. **チャット**タブに移動
2. なんでも質問してみて〜
3. ギャル語で答えが返ってくるよ💕

### Step 4: 性能をチェック 💯

1. **採点**タブに移動
2. 評価したいメトリクスを選択
3. 評価スタート！結果をチェックしてね✨

> [!NOTE]
> 実は資料をアップロードしなくても通常のチャットもできるよ〜

## 🛠️ セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/molmolkky/chat-gal-app
```

### 2. 仮想環境を作成

```bash
python -m venv venv
source venv/bin/activate
```

### 3. 依存関係をインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数を設定

`.env`ファイルを作成して、Azure OpenAIの設定を記入してね💕

```env
AZURE_OPENAI_EMBEDDING_ENDPOINT=your_embedding_endpoint
AZURE_OPENAI_EMBEDDING_API_KEY=your_embedding_api_key
AZURE_OPENAI_EMBEDDING_API_VERSION=your_embedding_api_version
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=your_embedding_deployment_name
AZURE_OPENAI_CHAT_ENDPOINT=your_chat_endpoint
AZURE_OPENAI_CHAT_API_KEY=your_chat_api_key
AZURE_OPENAI_CHAT_API_VERSION=your_chat_api_version
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_chat_deployment_name
```

### 5. アプリを起動

```bash
streamlit run app.py
```

## 📁 プロジェクト構成

```tree
ChatGAL/
├── .streamlit
│   └── config.toml     # 見た目やフォントを設定
├── app.py              # メインアプリ
├── backend
│   ├── __init__.py
│   ├── chat.py             # チャット機能
│   ├── evaluation.py       # 評価機能
│   ├── upload.py           # アップロード機能
│   └── utils
│       ├── __init__.py
│       └── clean_text_for_llm.py
├── config_manager.py       # 環境変数設定サイドバー
├── pages
│   ├── 1_chat_page.py          # チャットページ
│   ├── 2_upload_page.py        # アップロードページ
│   └── 3_evaluation_page.py    # 評価ページ
├── README.md
├── requirements.txt
├── search_settings.py          # 検索数サイドバー
├── static
│   └── Poppins-ThinItalic.ttf  # フォントたち
└── ui
    ├── __init__.py
    ├── chat_ui.py          # チャットUI
    ├── evaluation_ui.py    # 評価UI
    └── upload_ui.py        # アップロードUI
```

## 🔧 技術スタック

- **Frontend**: Streamlit 🌟
- **LLM**: Azure OpenAI GPT4.1 🧠
- **Embeddings**: Azure OpenAI text-embedding-3-large 📊
- **Vector Store**: LangChain InMemoryVectorStore 💾
- **Evaluation**: RAGAS 📈
- **Visualization**: Plotly 📊

## 💡 特徴

### 🎀 ギャル語AI

- システムプロンプトでギャル語に変換
- 絵文字たっぷりで楽しい会話

### 🔍 スマートRAG

- PDFから自動でチャンク分割
- ベクトル検索で関連情報を取得
- 文脈を考慮した回答生成

### 📊 詳細評価

- 4つのメトリクスで多角的評価
- 時系列チャートで変化を追跡
- CSV出力で詳細分析も可能

## 🚨 注意事項

- Azure OpenAIのAPIキーが必要だよ〜💳
- PDFファイルのサイズが大きいと時間かかるかも⏰
- 評価機能はRAGASを使ってるから、ちょっと重いよ💦

## 📄 ライセンス

自由に使ってね〜✨

💕 楽しいチャットライフを〜🦄✨
