from splitwise import create_splitwise_expense
from ocr import extract_amount_from_pdf
import os

pdf_path = os.path.abspath('elmaildata\\examplepdf.pdf')
print extract_amount_from_pdf(pdf_path)
create_splitwise_expense(1.0)

print "helo"