# PDF Invoice Processor

## Overview

This Python script simplifies the process of updating invoice amounts in PDFs using a question-answering model and a 15% margin calculation. The tool performs the following steps:

1. **Extracting Invoice Amount**: Given an input PDF invoice, the script utilizes a question-answering model to extract the invoice amount.

2. **Calculating Margin**: The script calculates a 15% margin on the extracted invoice amount.

3. **Generating Updated PDF**: Using the extracted amount and margin, the tool generates a new PDF with the updated total.

## Usage Example

```shell
python process_invoice.py input_invoice.pdf
