import os
import PyPDF2
import time

from progress.bar import Bar
from typing import Literal, List
from utils.bcolors import bcolors


class RetrievedFilesType:

    def __init__(self, name: str, path: os.path, created_at: str, last_modified_at: str):

        self.name = name
        self.path = path
        self.created_at = created_at,
        self.last_modified_at = last_modified_at

class ResizePDF:

    def __init__(self, input_path: str, output_path: str, desired_format: Literal["A2","A3", "A4", "A5", "L13"], order_by: Literal["creation_date", "last_modification_date", "name"]="name") -> None:

        self.__input_path = input_path
        self.__input_filename = os.path.basename(input_path)
        self.__output_path = f'{output_path}{self.__input_filename}'
        self.__desired_format = desired_format
        self.__desired_doc_type = 'pdf'
        self.__order_by = order_by

        self.__MEASEURE_POINTS = 2.83464567

        self.__formats = {
            "A2": (420, 594),
            "A3": (297, 420),
            "A4": (210, 297),
            "A5": (148, 210)
        }

        self.__desired_dimensions = self.mm_to_point_transformation()

        os.makedirs(output_path, exist_ok=True)

        self.__report = []

    def is_pdf(self, file: str) -> bool:
        """Check if a file is a PDF.

        Args:
            file (str): The name of the file.

        Returns:
            bool: True if the file is a PDF, False otherwise.
        """

        filename = file or self.__input_filename

        return filename.split('.')[-1].lower() == self.__desired_doc_type

    def retrieve_pdfs_per_folder(self) -> List[RetrievedFilesType]:
        """Retrieve a list of PDF files in the input folder.

        Returns:
            list: List of PDF file paths.
        """

        document_list = os.listdir(self.__input_path)

        pdf_list = []

        for doc in document_list:

            if self.is_pdf(doc):

                created_at, last_modified_at = self.get_last_modified_date(f'{self.__output_path}{doc}')

                pdf_list.append(
                    {
                        "name": doc,
                        "path": f'{self.__output_path}{doc}',
                        "created_at": created_at,
                        "last_modified_at": last_modified_at
                    }
                )

        ordenated_pdf_list = self.ordenate_files(pdf_list)

        self.print_documents(ordenated_pdf_list)

        #print(pdf_list)

        return ordenated_pdf_list
    
    # def __handle_scale_factor(self, width: float, height: float):

    def ordenate_files(self, pdf_list: List[RetrievedFilesType]) -> List[RetrievedFilesType]:
        if self.__order_by == "name":
            return sorted(pdf_list, key=lambda x: x["name"])
        elif self.__order_by == "creation_date":
            return sorted(pdf_list, key=lambda x: x["created_at"])
        elif self.__order_by == "last_modification_date":
            return sorted(pdf_list, key=lambda x: x["last_modified_at"])
        else:
            return pdf_list
        

    def print_documents(self, pdf_list: List[RetrievedFilesType]) -> None:
        print("List of Retrieved PDF Documents:")
        print("{:<30} {:<50} {:<20} {:<20}".format("Name", "Path", "Created At", "Last Modified At"))
        print("-" * 120)
        for doc in pdf_list:
            print("{:<30} {:<50} {:<20} {:<20}".format(doc["name"], doc["path"], doc["created_at"], doc["last_modified_at"]))



    def get_last_modified_date(self, path: os.path) -> object:

        creation_time = os.path.getctime(path)
        lastmodified_time = os.path.getmtime(path)

        creation_time = time.ctime(creation_time)
        lastmodified_time = time.ctime(lastmodified_time)

        return  creation_time, lastmodified_time
            
    def mm_to_point_transformation(self) -> tuple[float, float]:

        final_width = round(
            self.__formats[self.__desired_format][0] * self.__MEASEURE_POINTS)

        final_height = round(
            self.__formats[self.__desired_format][1] * self.__MEASEURE_POINTS)

        return (final_width, final_height)
    

    def get_scale_factor(self, original_dimension: tuple[float, float]) -> tuple[float, float]:

        scale_factor_w = self.__desired_dimensions[0] / original_dimension[0]
        scale_factor_y = self.__desired_dimensions[1] / original_dimension[1]

        scale_factor = (
            scale_factor_w, 
            scale_factor_y
        )

        #print(scale_factor)

        return scale_factor


    def __handle_resize(
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

                reader = pypdf.PdfReader(file)
                writer = pypdf.PdfWriter()

                for page_number in range(len(reader.pages)):

                    page = reader.pages[page_number]

                    original_height = float(page.mediabox.height)
                    original_width = float(page.mediabox.width)

                    original_dimension = (original_width, original_height)

                    #print('Original dimensions', original_width, original_height)

                    # page.cropbox.scale(5, 5)

                    scale_factor = self.get_scale_factor(original_dimension)

                    page.scale(scale_factor[0], scale_factor[1])

                    page.mediabox.lower_left = (0, 0)
                    page.mediabox.upper_right = self.__desired_dimensions  # A4 size: 210 x 297 mm

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

        progress_bar = Bar(
            f'{bcolors.OKBLUE}Processing {self.__input_filename}...', max=len(pdf_list))

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

            print(
                f'{bcolors.FAIL}The file ({self.__input_filename}) is not a PDF or is not supported.')

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

                # Resize the single PDF file
                self.resize_a_single_file(pdf_list[0])
            elif len(pdf_list) > 1:

                self.resize_pipeline(pdf_list)  # Resize multiple PDF files
            else:

                print(f"{bcolors.WARNING}No PDF files found in the directory.")
        else:

            print(f"{bcolors.WARNING}Invalid input path.")


""" resizer = ResizePDF(
    'J:/arquivos_digitalizados/engenharia_agronomica/em_andamento/Engenharia_agronomica_2014(2)/',
    'J:/arquivos_digitalizados/engenharia_agronomica/finalizados/Engenharia_agronomica_2014(2)/',
    "A4"
) """


resizer = ResizePDF(
    'J:/arquivos_digitalizados/engenharia_agronomica/em_andamento/Engenharia_agronomica_2016(2)/',
    'J:/arquivos_digitalizados/engenharia_agronomica/finalizados/Engenharia_agronomica_2016(2)/',
    "A4"
)
#resizer.resize()

resizer.retrieve_pdfs_per_folder()