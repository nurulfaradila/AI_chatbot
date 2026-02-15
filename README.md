# 🦤 DoDo - Your Private Document Assistant

Hi there! 👋 Welcome to **DoDo**, your new friendly local chatbot that knows your documents inside out.

Ever wished you could just *ask* your PDF a question instead of scrolling through 50 pages? That's exactly what DoDo does. And the best part? It runs 100% on your computer. Your files never leave your machine, so everything stays **private, secure, and under your control**. 

No subscriptions, no hidden fees, just you and your docs.

---

## 🌟 Why DoDo?

-   **🔒 100% Private**: Your sensitive documents never touch the cloud.
-   **🧠 Smart RAG Technology**: Uses Retrieval-Augmented Generation (RAG) to find the *exact* answer from your specific docs.
-   **⚡ Fast & Local**: Powered by efficient local AI models (Phi via Ollama).
-   **📂 Easy Peasy**: Just drop a file in, click "Rebuild", and start chatting!

---

## 🚀 Getting Started

Setting up DoDo is super simple. Here's how to get your own assistant running in minutes:

### 1. Install the Brain (Ollama)
DoDo needs a brain to work! We use **Ollama** for this.
1.  Download and install it from [ollama.com](https://ollama.com).
2.  Once installed, open your terminal and run this command to grab the brain model:
    ```bash
    ollama pull phi
    ```

### 2. Set Up the Project
Clone this repo or download the code, then navigate to the folder:

```bash
cd /path/to/your/project
```

Now, let's get the environment ready:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run DoDo!
You're almost there! Start the application with this command:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Now open your browser and go to: **[http://localhost:8000](http://localhost:8000)** 🎉

---

## 📖 How to Use

1.  **Drop Files**: Put any `.pdf` or `.txt` files you want to chat with into the `data/documents/` folder.
2.  **Teach DoDo**: In the web interface, click the **"Rebuild Index"** button. This teaches DoDo about your new files.
3.  **Chat**: Ask away! Try questions like:
    -   "Summarize the introduction."
    -   "What does the report say about Q3 sales?"
    -   "List the key takeaways."

---

## 🛠️ Tech Stack (The Geeky Stuff)

For those curious about what's under the hood:
-   **Backend**: Python & FastAPI (Lighting fast!)
-   **AI Engine**: Ollama running the Phi model.
-   **Search**: FAISS (Facebook AI Similarity Search) & Sentence-Transformers for finding the right context.
-   **Frontend**: Simple HTML/JS for a clean experience.

---

## 🆘 Troubleshooting

**"I don't get any answers!"**
> Did you remember to put files in `data/documents/` and click "Rebuild Index"? DoDo can't read what it hasn't indexed!

**"Connection Error?"**
> Make sure Ollama is running in the background. It needs to be active for DoDo to think.

---

## 📜 License
MIT License. Feel free to use and modify!

