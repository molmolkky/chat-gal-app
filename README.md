# 🎀✨ ChatGAL ✨🎀

> **超カワイイRAGチャットボット💕 ギャル語で質問に答えちゃうよ〜🦄**

## 💎 これなに？

ChatGALは、PDFファイルをアップロードして、その内容について**ギャル語**で教えてくれちゃう超キュートなチャットボットだよ〜✨

- 📚 **RAG（Retrieval-Augmented Generation）** でスマートに回答
- 🎯 **RAGAS評価** で性能もバッチリチェック
- 💅 **ギャル語** で楽しくおしゃべり
- 🌈 **Streamlit** でサクサク動く

## 🖼️ アプリのスクショはこんな感じ

<img width="1800" height="1004" alt="Image" src="https://github.com/user-attachments/assets/6cf6cd5e-e985-42cd-a900-85c3761b8d27" />

<img width="1800" height="1004" alt="Image" src="https://github.com/user-attachments/assets/3d675ebf-5cd3-4afe-a57d-c8a6276380c9" />

<img width="1800" height="1004" alt="Image" src="https://github.com/user-attachments/assets/d1cc6655-e948-4fc4-a2fd-c0dc27094e41" />

<img width="1800" height="1004" alt="Image" src="https://github.com/user-attachments/assets/ec6068cd-e4d6-4d1d-a966-51462269f4c1" />

<img width="1800" height="1004" alt="Image" src="https://github.com/user-attachments/assets/0f743594-2823-47c2-8271-fc3d5293a9bc" />

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
├── app.py                 # メインアプリ
├── config.py              # 設定ファイル
├── requirements.txt       # 依存関係
├── .env                      # 環境変数設定
├── backend/                  # バックエンド処理
│   ├── chat.py           # チャット機能
│   ├── upload.py         # アップロード処理
│   └── evaluation.py     # 評価機能
├── ui/                       # UI コンポーネント
│   ├── chat_ui.py        # チャットUI
│   ├── upload_ui.py      # アップロードUI
│   └── evaluation_ui.py  # 評価UI
└── pages/                    # Streamlitページ
    ├── 1_chat_page.py       # チャットページ
    ├── 2_upload_page.py     # アップロードページ
    └── 3_evaluation_page.py # 評価ページ
```

## 🎯 使い方

### Step 1: 資料をアップ 📚

1. **資料アップ**ページに移動
2. PDFファイルを選択してアップロード
3. 処理完了まで待つ（ちょっと時間かかるかも💦）

### Step 2: チャットで質問 💬

1. **チャット**タブに移動
2. なんでも質問してみて〜
3. ギャル語で答えが返ってくるよ💕

### Step 3: 性能をチェック 💯

1. **採点**タブに移動
2. 評価したいメトリクスを選択
3. 評価スタート！結果をチェックしてね✨

> [!NOTE]
> 実は資料をアップロードしなくても通常のチャットもできるよ〜

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
