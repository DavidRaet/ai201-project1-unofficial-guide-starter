import gradio as gr
from dotenv import load_dotenv

from src.config import TOP_K
from src.generate import generate_response
from src.vectorstore import make_collection, make_persistent_client, retrieve

load_dotenv()

_client = make_persistent_client()
_collection = make_collection(_client)


def query_rag(message: str, history: list) -> tuple[list, str]:
    if not message.strip():
        return history, ""
    chunks = retrieve(message, _collection, k=TOP_K)
    answer = generate_response(message, chunks)
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer},
    ]
    return history, ""


VASSAR_CSS = """
:root {
    --vc-burgundy: #8C1F3B;
    --vc-dark:     #5C0F25;
    --vc-mid:      #7A1A33;
    --vc-cream:    #F5F0E8;
}

/* ── Page background ─────────────────────────────── */
body,
.gradio-container,
.main,
footer {
    background: var(--vc-dark) !important;
    color: var(--vc-cream) !important;
}

/* ── Title ───────────────────────────────────────── */
.app-title {
    color: var(--vc-cream) !important;
    font-weight: 300 !important;
    letter-spacing: 0.07em !important;
    text-align: center !important;
    font-size: 2.2rem !important;
    padding: 2rem 0 0.5rem !important;
    margin: 0 !important;
}

/* ── Chat window ─────────────────────────────────── */
[data-testid="chatbot"],
.chatbot {
    background: var(--vc-burgundy) !important;
    border: 1px solid var(--vc-mid) !important;
}

/* ── Message bubbles ─────────────────────────────── */
.message,
.prose {
    color: var(--vc-cream) !important;
}

.message.assistant,
[data-testid="bot"] {
    background: var(--vc-mid) !important;
}

.message.user,
[data-testid="user"] {
    background: var(--vc-dark) !important;
    border: 1px solid var(--vc-mid) !important;
}

/* ── Input textbox ───────────────────────────────── */
textarea {
    background: var(--vc-burgundy) !important;
    color: var(--vc-cream) !important;
    border-color: var(--vc-mid) !important;
}

textarea::placeholder {
    color: rgba(245, 240, 232, 0.45) !important;
}

/* ── Submit button ───────────────────────────────── */
.submit-btn,
button.submit-btn {
    background: var(--vc-cream) !important;
    color: var(--vc-dark) !important;
    border: none !important;
    font-size: 1.3rem !important;
}

.submit-btn:hover {
    background: #e8e3db !important;
}

/* ── Panels / containers ─────────────────────────── */
.block,
.wrap,
.panel,
.form,
.gap {
    background: var(--vc-burgundy) !important;
    border-color: var(--vc-mid) !important;
}
"""

with gr.Blocks(fill_height=True) as demo:
    gr.HTML('<h1 class="app-title">vccs-inquiries</h1>')

    chatbot = gr.Chatbot(
        height=520,
        render_markdown=True,
        show_label=False,
        placeholder="Responses will appear here.",
    )

    with gr.Row():
        textbox = gr.Textbox(
            placeholder="Ask anything about Vassar CS courses and professors...",
            container=False,
            show_label=False,
            scale=9,
            autofocus=True,
        )
        send_btn = gr.Button("→", elem_classes=["submit-btn"], scale=1, min_width=60)

    send_btn.click(query_rag, [textbox, chatbot], [chatbot, textbox])
    textbox.submit(query_rag, [textbox, chatbot], [chatbot, textbox])

if __name__ == "__main__":
    demo.launch(css=VASSAR_CSS)
