import streamlit as st
import pandas as pd
from io import BytesIO

# File upload
file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if file:
    file_ext = "." + file.name.split(".")[-1].lower()

    # Read file into DataFrame
    if file_ext == ".csv":
        df = pd.read_csv(file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(file)
    else:
        st.error("Unsupported file format!")
        st.stop()

    # Conversion options
    st.subheader("⟲ Conversion Options")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()

        # Convert based on selected type
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False, engine='openpyxl')
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        buffer.seek(0)

        # Download button
        st.download_button(
            label=f"⇩ Download {file_name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type,
        )

        st.success("🎉 All files processed!️") 
        