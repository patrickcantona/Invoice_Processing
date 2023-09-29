import fitz
import os
import re
from transformers import pipeline
from rapidfuzz import fuzz

pipe = pipeline("document-question-answering", model="naver-clova-ix/donut-base-finetuned-docvqa")
image_data_folder = "invoices-images/"


def convert_pdf_to_images(pdf_file):
    try:
        # Obtenir le nom du document sans l'extension
        base_name = os.path.splitext(os.path.basename(pdf_file))[0]
        
        # Créer le dossier de sortie dans un dossier existant
        output_folder = os.path.join(image_data_folder, base_name)
        os.makedirs(output_folder, exist_ok=True)

        # Ouvrir le fichier PDF
        pdf_document = fitz.open(pdf_file)

        # Extraire chaque page du PDF sous forme d'image
        for page_number, page in enumerate(pdf_document):
            image = page.get_pixmap()
            image_path = os.path.join(output_folder, f"page-{page_number + 1}.png")
            
            image.save(image_path)


        return image_path

        # f"Conversion réussie : {pdf_document.page_count} images créées dans {output_folder}."
    except Exception as e:
        return f"Erreur : {str(e)}"

def extract_total_amount(image_path):
  question_amount = "What is the total amount?"
  total_amount_result = pipe(image=image_path, question=question_amount, max_length=10)
  answer = total_amount_result[0]['answer']

  return answer

def extract_and_convert_number(input_string):
    try:
        # Essayer de convertir la chaîne en un entier
        integer_number = int(input_string)
        return integer_number
    except ValueError:
        # Si la conversion en entier échoue, essayez d'extraire un nombre décimal
        decimal_match = re.search(r'[\d\s,.-]+', input_string)

        if decimal_match:
            # Si une correspondance est trouvée, récupérez-la
            decimal_str = decimal_match.group()
            
            # Supprimez les espaces de la chaîne
            decimal_str = decimal_str.replace(' ', '')
            
            # Remplacez toutes les virgules par des points
            decimal_str = decimal_str.replace(',', '.')
            
            # Supprimez le premier point s'il y en a deux
            if decimal_str.count('.') > 1:
                decimal_str = decimal_str.replace('.', '', 1)

            try:
                # Convertissez la chaîne en un nombre à virgule flottante
                decimal_number = float(decimal_str)
                # Formatez le nombre avec deux décimales
                formatted_decimal = '{:.2f}'.format(decimal_number)

                return formatted_decimal
            except ValueError:
                return "Error: Unable to convert the extracted decimal to a float."
        else:
            return "Error: No valid number found in the input string."


def calculate_margin(input_value):
    try:
        # Convertir la valeur d'entrée en float au cas où ce ne serait pas déjà fait
        input_float = float(input_value)
        
        # Calculer la marge de 15 %
        margin = round(input_float * 1.15, 2)
        return margin
    except ValueError:
        return "Error: Invalid input value."


def process_answer(answer, total_amount_with_margin):
    if ',' in answer:
        # Si la virgule est présente dans la réponse
        total_amount_with_margin_text = str(total_amount_with_margin).replace(".", ",")
    else:
        # Sinon, utilisez la virgule par défaut
        total_amount_with_margin_text = str(total_amount_with_margin)

    return total_amount_with_margin_text


# Fonction pour calculer le ratio entre un mot fixe et une liste de mots
def calculate_ratio(word_list, fixed_word):
    highest_ratio = 0
    best_match = ""

    for word in word_list:
        ratio = fuzz.ratio(fixed_word, word)
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = word

    return highest_ratio, best_match