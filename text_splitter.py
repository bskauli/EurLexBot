from bs4 import BeautifulSoup



def print_html_headers(file_path):
    try:
        with open(file_path, 'r') as html:
            # Find all the paragraphs in the HTML document
            soup = BeautifulSoup(html, 'html.parser')

            paragraphs = soup.find_all('p')

            # Extract the text content from each paragraph and store in a list
            paragraph_texts = [paragraph.text for paragraph in paragraphs]

            # Print the list of paragraph texts
            for text in paragraph_texts:
                print('-----------------')
                print(text)
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")

file_path = './dlt_pilot.html'
print_html_headers(file_path)
