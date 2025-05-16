# simple_chat_app - セットアップ手順

このプロジェクトでは、`streamlit` と `langchain` を使用してチャットアプリを構築します。
**古いバージョンのlangchain-community** を使用するため、仮想環境のセットアップが必須です。

## 🔧 前提条件

* Python 3.10〜3.12 がインストールされていること
* Git Bash または PowerShell が使用できること

## 📝 セットアップ手順

### 1️⃣ プロジェクトフォルダに移動

```bash
cd /c/git/simple_chat_app
```

### 2️⃣ 仮想環境を作成

```bash
python -m venv venv
```

### 3️⃣ 仮想環境をアクティブにする

**Git Bash または bash:**

```bash
source venv/Scripts/activate
```

**PowerShell の場合:**

```bash
venv\Scripts\Activate.ps1
```

成功すると、プロンプトの先頭に `(venv)` が表示されます。

### 4️⃣ pip を最新版にアップグレード

```bash
python -m pip install --upgrade pip
```

または

```bash
pip install --upgrade pip
```

アップグレード後、バージョン確認：

```bash
pip --version
```

例：`pip 24.0` などと表示されればOK。

### 5️⃣ 必要パッケージをインストール

```bash
pip install streamlit
pip install langchain
pip install langchain-community
pip install langchain-ollama
```

または、`requirements.txt` がある場合：

```bash
pip install -r requirements.txt
```

### 6️⃣ Streamlit アプリの実行

```bash
streamlit run simple_chat_app.py
```

ブラウザでアプリが起動します。

---

## 📝 仮想環境を終了するには

```bash
deactivate
```
