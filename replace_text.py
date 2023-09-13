import fitz
import sys

def open_pdf(input_pdf, new_text, old_text, output_pdf):
    doc = fitz.open(input_pdf)

    page = doc[0] 
    # list of rectangles where to replace

    hits = page.search_for(old_text)  
    for rect in hits:
        point = (rect[0], rect[-1])

        page.draw_rect(rect, fill=(1,), color=(1, 1, 1))
        page.insert_text(point, new_text, fontsize=11, fontname='helv')

    doc.save(output_pdf)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python your_script.py input_pdf new_text old_text output_pdf")
    else:
        input_pdf = sys.argv[1]
        new_text = sys.argv[2]
        old_text = sys.argv[3]
        output_pdf = sys.argv[4]
        open_pdf(input_pdf, new_text, old_text, output_pdf)
