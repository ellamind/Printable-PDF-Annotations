import gradio as gr
import tempfile
from pathlib import Path
from annotate_pdf import annotate_pdf

def process_pdf(pdf_file_path, search_terms):
    # Create a temporary directory to store our files
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Read the uploaded PDF
        with open(pdf_file_path, "rb") as input_file:
            pdf_content = input_file.read()
        
        # Save the PDF content to a temporary file
        temp_input_path = Path(tmpdirname) / "input.pdf"
        with open(temp_input_path, "wb") as f:
            f.write(pdf_content)
        
        # Create output path
        temp_output_path = Path(tmpdirname) / "output.pdf"
        
        # Split search terms and remove any empty strings
        search_list = [term.strip() for term in search_terms.split(',') if term.strip()]
        
        # Annotate the PDF
        annotate_pdf(temp_input_path, search_list, temp_output_path)
        
        # Create a new temporary file to store the output
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        output_file.close()
        
        # Copy the annotated PDF to the new temporary file
        Path(temp_output_path).rename(output_file.name)
    
    return output_file.name

# Create the Gradio interface
iface = gr.Interface(
    fn=process_pdf,
    inputs=[
        gr.File(label="Upload PDF"),
        gr.Textbox(label="Enter search terms (comma-separated)")
    ],
    outputs=gr.File(label="Annotated PDF"),
    title="PDF Annotator",
    description="Upload a PDF and enter search terms to create an annotated version of the PDF."
)

# Launch the app
iface.launch()