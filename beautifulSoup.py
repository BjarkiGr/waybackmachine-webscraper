from bs4 import BeautifulSoup
import os
import csv

current_directory = os.path.dirname(__file__)
html_directory = os.path.join(current_directory)
output_csv_file = os.path.join(current_directory, 'extracted_data.csv')
your_selector = '[data-tarifcat="2657"]'

with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')

    csv_writer.writerow(["filename", "Category", "td1", "td2"])

    for filename in os.listdir(html_directory):
        if filename.endswith(".html"):
            file_path = os.path.join(html_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            result_elements = soup.select(your_selector)

            for element in result_elements:
                tbody_elements = element.select('table tbody')
                for i, tbody in enumerate(tbody_elements):
                    tr_elements = tbody.select('tr')
                    if len(tr_elements) >= 3:
                        third_tr = tr_elements[2]
                        td_elements = third_tr.find_all('td')[:2]
                        td1, td2 = [td.get_text(strip=True) for td in td_elements]
                        category = "BAF" if i == 0 else "LSS"
                        csv_writer.writerow([filename[:-5], category, td1, td2])
