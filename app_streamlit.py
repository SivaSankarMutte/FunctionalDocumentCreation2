import streamlit as st
import tempfile
import os
from generate_doc import generate_functional_doc

st.set_page_config(page_title="Functional Doc Generator", page_icon="📄", layout="wide")

st.title("📄 Functional Documentation Generator")
st.write("Upload a ZIP of your codebase to generate a functional documentation report.")

uploaded_file = st.file_uploader("Upload ZIP file", type=["zip"])

if uploaded_file is not None:
    with st.spinner("Generating documentation... This may take a few minutes."):
        try:
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # Call your function (no workdir!)
            result = generate_functional_doc(tmp_path, output_dir="output")

            # Since your function currently returns a string, 
            # better to modify it to return (md_path, doc_path)
            # but for now we’ll just parse the output
            md_path = os.path.join("output", "functional_doc.md")
            docx_path = os.path.join("output", "functional_doc.docx")

            # Download buttons
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            st.download_button(
                "⬇️ Download as Markdown",
                md_content,
                file_name="functional_doc.md",
                mime="text/markdown"
            )

            with open(docx_path, "rb") as f:
                st.download_button(
                    "⬇️ Download as DOCX",
                    f,
                    file_name="functional_doc.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            # Preview in Streamlit
            st.subheader("📖 Documentation Preview")
            st.markdown(md_content)

        except Exception as e:
            st.error(f"Error: {e}")
