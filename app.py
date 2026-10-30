import os
import gradio as gr
from groq import Groq


def translate_text(text):
    if not text.strip():
        return "Введіть текст для перекладу."

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return "API-ключ не налаштовано."

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "Translate English text into Ukrainian. Return only the translation, without explanations."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.2,
        max_completion_tokens=1024
    )

    return response.choices[0].message.content.strip()


with gr.Blocks() as demo:
    gr.Markdown("# English → Ukrainian Translator")
    gr.Markdown(
        "Перекладач тексту з англійської на українську за допомогою LLM."
    )

    input_text = gr.Textbox(
        label="Англійський текст",
        placeholder="Введіть текст англійською...",
        lines=5
    )

    translate_button = gr.Button(
        "Перекласти",
        variant="primary"
    )

    output_text = gr.Textbox(
        label="Український переклад",
        lines=5,
        interactive=False
    )

    translate_button.click(
        fn=translate_text,
        inputs=input_text,
        outputs=output_text
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 10000))
    )
