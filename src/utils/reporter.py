Number = float | int

def create_report(
        content: Number | str,
        writting_path: str,
):
    with open('report.txt',  'w') as report_file:

        report_file.write(content)
    
    
