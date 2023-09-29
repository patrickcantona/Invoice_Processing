from flask import Flask, request, render_template, send_file
from process_invoice import process_pdf  # Importez votre fonction process_pdf depuis votre script existant
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Vérifiez si un fichier a été téléchargé
        if "pdf_file" not in request.files:
            return "No file part"
        
        pdf_file = request.files["pdf_file"]

        # Vérifiez si le fichier a un nom valide
        if pdf_file.filename == "":
            return "No selected file"

        # Vérifiez si l'extension du fichier est PDF
        if not pdf_file.filename.endswith(".pdf"):
            return "Invalid file type"

        # Enregistrez le fichier téléchargé temporairement
        uploaded_pdf_path = "uploaded.pdf"
        pdf_file.save(uploaded_pdf_path)

        # Traitez le fichier PDF
        process_pdf(uploaded_pdf_path)

        # Renvoyez le fichier généré en téléchargement
        generated_pdf_path = "processed_invoices/processed_" + os.path.basename(uploaded_pdf_path)
        return send_file(generated_pdf_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
