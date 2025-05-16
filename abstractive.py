from transformers import pipeline

# You can reuse the summarizer with a large model and appropriate tokenizer limits
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def abstractive_summary(text, min_len=100, max_len=250):  # Increase limits
    # If text is long, split it in chunks
    if len(text.split()) > 500:
        text = text[:2000]  # Truncate very long texts if needed (or split into parts)

    summary = summarizer(text, min_length=min_len, max_length=max_len, do_sample=False)
    return summary[0]['summary_text']
