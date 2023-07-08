import os
import html

def create_website(payload_file):
    # Get the directory path of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Open the payload file and read all the lines
    with open(payload_file, 'r', encoding='utf-8', errors='ignore') as file:
        payloads = file.read().splitlines()

    # Create the HTML content
    html_content = '<html>\n<head>\n<style>\n'
    html_content += 'body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center;}\n'
    html_content += '.payload-container { text-align: center; }\n'
    html_content += '.payload { padding: 10px; margin-bottom: 10px; background-color: #f0f0f0; }\n'
    html_content += '</style>\n</head>\n<body>\n'
    html_content += '<h1 id="h1_element">This is a h1 element</h1>\n'
    html_content += '<div class="payload-container">\n'
    
    for payload in payloads:
        payload = html.escape(payload.strip())
        html_content += '<div class="payload">{}</div>\n'.format(payload)

    html_content += '</div>\n</body>\n</html>'

    # Save the HTML content to a file in the script's directory
    html_file_path = os.path.join(script_dir, 'xss_website.html')
    with open(html_file_path, 'w') as file:
        file.write(html_content)

    print('Website created successfully.')
    print('HTML file saved at:', html_file_path)




# Create the website
create_website('payloads/small_payload.txt')