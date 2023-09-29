import fitz
import sys
import os
from detect_amount import *
import warnings

# Désactiver tous les avertissements (warnings)
warnings.filterwarnings("ignore")

processed_invoices_folder = "processed_invoices/"

def process_pdf(input_pdf):
    doc = fitz.open(input_pdf)


    page = doc[0]
    extracted_text =  page.get_text()
    word_list = extracted_text.split()


    file_name = os.path.basename(input_pdf)
    output_filename =  "processed_" + file_name
    output_pdf = os.path.join(processed_invoices_folder, output_filename)

    image_path =  convert_pdf_to_images(input_pdf)
    answer =  extract_total_amount(image_path)
    
    total_mount = extract_and_convert_number(answer)

    total_amount_with_margin = calculate_margin(total_mount)

    total_amount_with_margin_text = process_answer(answer, total_amount_with_margin )

    # Calculez le partial_ratio le plus élevé et le mot équivalent
    highest_ratio, best_match = calculate_partial_ratio(word_list, answer)

    answer = answer if answer in word_list else best_match

    print("The total amount detected is : " , answer)
    print(f"the best match word : {best_match}")
    print(f"the highest ratio : {highest_ratio}")

    print("The total amount converted is : " , total_mount)
    print("The total amount with margin is : " , total_amount_with_margin_text)

    # list of rectangles where to replace

 

    hits = page.search_for(answer)  

    for rect in hits:
        point = (rect[0], rect[-1])

        page.draw_rect(rect, fill=(1,), color=(1, 1, 1))
        page.insert_text(point, total_amount_with_margin_text, fontsize=11, fontname='helv')

    
    doc.save(output_pdf)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py input_pdf")
    else:
        input_pdf = sys.argv[1]
        process_pdf(input_pdf)
