import streamlit as st
import matplotlib.pyplot as plt
import pdfplumber, io
from docx import Document
def extract_text(file):
    data = file.read()
    if file.name.endswith(".pdf"):
        return ' '.join([p.extract_text() for p in pdfplumber.open(io.BytesIO(data)).pages if p.extract_text()])
    return ' '.join([p.text for p in Document(io.BytesIO(data)).paragraphs if p.text.strip()])

def split_into_sentences(text):
    text = text.replace('?', '.').replace('!', '.')  
    sentences = text.split('.')
    return [s.strip() for s in sentences if s.strip()]


def get_sentence_lengths(sentences):
    return [len(s.split()) for s in sentences]


st.set_page_config(layout="centered")
st.title("📏 Sentence Length Analyzer")

uploaded = st.file_uploader("Upload PDF or Word Document", type=["pdf", "docx"])

if uploaded:
    text = extract_text(uploaded)
    sentences = split_into_sentences(text)
    lengths = get_sentence_lengths(sentences)

    st.write(f"**Total Sentences:** {len(sentences)}")
    st.write(f"**Average Sentence Length:** {sum(lengths) / len(lengths):.2f} words")

    st.subheader("Histogram of Sentence Lengths")
    fig1, ax1 = plt.subplots()
    ax1.hist(lengths, bins=20, color='orange', edgecolor='black')
    ax1.set_xlabel("Words per Sentence")
    ax1.set_ylabel("Number of Sentences")
    ax1.set_title("Sentence Length Distribution")
    st.pyplot(fig1)

    st.subheader("Sentence Length Over Document")
    fig2, ax2 = plt.subplots()
    ax2.plot(range(1, len(lengths)+1), lengths, marker='o', linestyle='-', color='blue')
    ax2.set_xlabel("Sentence Index")
    ax2.set_ylabel("Length (words)")
    ax2.set_title("Sentence Length Trend")
    st.pyplot(fig2)
