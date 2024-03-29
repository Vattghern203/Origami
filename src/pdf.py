import PyPDF2

from typing import Literal

import os

from utils.bcolors import bcolors

from progress.bar import Bar

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
        self.__output_path = f'{output_path}{self.__input_filename}'

        print(self.__output_path)

        self.__desired_format = desired_format
        self.__desired_doc_type = 'pdf'

        self.__formats = {
            "A4": (210, 297)
        }

        os.makedirs(output_path, exist_ok=True)


    def is_pdf(self, file: str) -> bool:
        """Check if a file is a PDF.

        Args:
            file (str): The name of the file.

        Returns:
            bool: True if the file is a PDF, False otherwise.
        """

        filename = file or self.__input_filename

        return filename.split('.')[-1].lower() == self.__desired_doc_type
    

    def retrieve_pdfs_per_folder(self) -> list:
        """Retrieve a list of PDF files in the input folder.

        Returns:
            list: List of PDF file paths.
        """

        document_list = os.listdir(self.__input_path)

        pdf_list = []

        for doc in document_list:

            if self.is_pdf(doc): 
                
                pdf_list.append(
                    {
                        "name": doc,
                        "path": f'{self.__output_path}{doc}'
                    }
                )

        print(f'{bcolors.OKCYAN}{pdf_list}')

        return pdf_list


    def  __handle_resize(
            self, 
            pdf_file_path: str, 
            output_path: str
        ):
        """Resize a PDF file to the desired format.

        Args:
            pdf_file_path (str): The path to the PDF file.
        """

        try:

            print(f'{bcolors.OKBLUE} Processing [{self.__input_filename}]...')

            with open(pdf_file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()

                for page_number in range(len(reader.pages)):

                    page = reader.pages[page_number]
                    page.mediabox.lower_left = (0, 0)
                    page.mediabox.upper_right = (595, 842)  # A4 size: 210 x 297 mm

                    writer.add_page(page)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

                print(
                    f'{bcolors.OKGREEN}The PDF file ({self.__input_filename}) has been resized with success!'
                )

        except Exception as error:

            print(f'{bcolors.FAIL}An error occurred: ', error)

    def resize_pipeline(self, pdf_list: list) -> None:
        """Resize multiple PDF files in a batch.

        Args:
            pdf_list (list): List of PDF file paths.
        """

        print(f'{bcolors.OKBLUE}Converting {len(pdf_list)} files...')

        progress_bar = Bar(f'{bcolors.OKBLUE}Processing {self.__input_filename}...', max=len(pdf_list))

        for doc in pdf_list:

            progress_bar.next()
            
            self.__input_filename = doc["name"]

            self.__handle_resize(
                f'{self.__input_path}{doc["name"]}', doc["path"]
            )


        progress_bar.finish()

    def resize_a_single_file(self) -> None:
        """Resize a single PDF file.

        If the input file is not a PDF or is not supported, print an error message.
        """

        if self.is_pdf(self.__input_filename):

            self.__handle_resize(self.__input_path, self.__output_path)

        else:

            print(f'{bcolors.FAIL}The file ({self.__input_filename}) is not a PDF or is not supported.')


    def resize(self) -> None:
        """Resize PDF files based on the input path.

        If the input path is a file, resize the single file.
        If the input path is a directory, resize all PDF files in the directory.
        """
    
        if os.path.isfile(self.__input_path):

            self.resize_a_single_file()  # Resize the single file

        elif os.path.isdir(self.__input_path):

            pdf_list = self.retrieve_pdfs_per_folder()  # Retrieve PDFs from the directory

            if len(pdf_list) == 1:

                self.resize_a_single_file(pdf_list[0])  # Resize the single PDF file
            elif len(pdf_list) > 1:

                self.resize_pipeline(pdf_list)  # Resize multiple PDF files
            else:

                print(f"{bcolors.WARNING}No PDF files found in the directory.")
        else:

            print(f"{bcolors.WARNING}Invalid input path.")


resizer = ResizePDF(
    'D:/Biblioteca/Documentos/Códigos/_intern_projects/paper-converter/to_convert/', 'D:/Biblioteca/Documentos/Códigos/_intern_projects/paper-converter/converted/',
    'A4'
)

resizer.resize()