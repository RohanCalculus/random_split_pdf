import streamlit as st
import PyPDF2
from io import BytesIO

def split_custom_pages_from_pdf(file, selected_pages):
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()
    total_pages = len(reader.pages)

    for page_num in selected_pages:
        if 1 <= page_num <= total_pages:
            writer.add_page(reader.pages[page_num - 1])
        else:
            st.warning(f"Page {page_num} is out of range. Skipping...")

    output_buffer = BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer

# Set up page
st.set_page_config(page_title="PDF Page Extractor", layout="centered", page_icon="🪄")

# Inject background CSS
st.markdown("""
    <style>
    body {
        background-image: url("https://live.staticflickr.com/5451/8762591634_f89de655a1_b.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    .stApp {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }

    .stTextInput>div>div>input {
        background-color: #000000aa;
        color: white;
    }

    .stFileUploader>div>div {
        background-color: #00000055;
        border-radius: 10px;
    }

    </style>
""", unsafe_allow_html=True)

# App content
st.title("📄 Extract Pages from PDF!")

uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf is not None:
    pages_input = st.text_input("Enter page numbers to extract (comma-separated, e.g., 1,3,5):")

    if pages_input:
        try:
            selected_pages = [int(p.strip()) for p in pages_input.split(",") if p.strip().isdigit()]
            output_pdf = split_custom_pages_from_pdf(uploaded_pdf, selected_pages)

            st.success("✅ Pages extracted successfully!")
            st.download_button(
                label="📥 Download Extracted PDF",
                data=output_pdf,
                file_name="extracted_pages.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
