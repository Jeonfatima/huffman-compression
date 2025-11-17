import streamlit as st
from Huffman import HuffmanCoding  # 👈 this imports your class
import os

st.title("📦 Huffman Compression & Decompression Tool")

option = st.radio("Choose an action:", ["Compress a file", "Decompress a file"])

if option == "Compress a file":
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        temp_path = "temp_input.txt"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Compress File"):
            h = HuffmanCoding(temp_path)
            output_path = h.compress()

            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Download Compressed File",
                    data=f,
                    file_name=os.path.basename(output_path),
                    mime="application/octet-stream"
                )
            st.success("✅ File successfully compressed!")

elif option == "Decompress a file":
    uploaded_file = st.file_uploader("Upload a .bin file", type=["bin"])

    if uploaded_file is not None:
        temp_path = "temp_compressed.bin"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Decompress File"):
            h = HuffmanCoding(temp_path)
            output_path = h.decompress(temp_path)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Download Decompressed File",
                    data=f,
                    file_name=os.path.basename(output_path),
                    mime="text/plain"
                )
            st.success("✅ File successfully decompressed!")
