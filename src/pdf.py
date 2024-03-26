import PyPDF2

from typing import Literal

import os

""" def resize_pdf_to_a4(input_path, output_path):
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            page.mediabox.lower_left = (0, 0)
            page.mediabox.upper_right = (595, 842)  # A4 size: 210 x 297 mm

            writer.add_page(page)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

# Example usage
input_file_path = 'essay.pdf'
output_file_path = f'converted/resized.pdf'

resize_pdf_to_a4(input_file_path, output_file_path)
print("PDF resized successfully.") """

class ResizePDF:

    def __init__(self, input_path: str, output_path: str, desired_format: Literal["A4", "A3", "L13"]) -> None:
        
        self.__input_path = input_path
        self.__input_filename = os.path.basename(input_path)
        self.__output_path = f'{output_path}/{self.__input_filename}'

        self.__desired_format = desired_format or 'A4'
        self.__desired_doc_type = 'pdf'

        self.__formats = {
            "A4": (210, 297)
        }

    
    def is_pdf(self) -> bool:

        return self.__input_filename.split('.')[-1].lower() == self.__desired_doc_type

    def resize_pdf_to_a4(self):

        if self.is_pdf():

            try:
                with open(self.__input_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    writer = PyPDF2.PdfWriter()

                    for page_number in range(len(reader.pages)):

                        page = reader.pages[page_number]
                        page.mediabox.lower_left = (0, 0)
                        page.mediabox.upper_right = (595, 842)  # A4 size: 210 x 297 mm

                        writer.add_page(page)

                    with open(self.__output_path, 'wb') as output_file:
                        writer.write(output_file)

                    print(f'The PDF file ({self.__input_filename}) has been resized with success!')

            except Exception as error:

                print('An error occurred: ', error)

        else:

            print(f'The file ({self.__input_filename}) is not a PDF or is not supported.')

resizer = ResizePDF(
    'to_convert/essay.pdf', 'converted', 'A4'
).resize_pdf_to_a4()