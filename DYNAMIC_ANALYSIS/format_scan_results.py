import json

global taint_results
taint_results = []

global not_taint_result
not_taint_results = []


def interpret_json_file(file_path):
    try:
        with open(file_path) as file:
            json_data = json.load(file)
            # Interpret the JSON data
            results = json_data['results']

            # split the data into taint and non_taint lists
            for result in results:
                if 'dataflow_trace' in result['extra']:
                    taint_results.append(result)
                    print(taint_results)
                else:
                    not_taint_results.append(result)


    except FileNotFoundError:
        print("File not found: " + file_path)
    except json.JSONDecodeError:
        print("Invalid JSON format in file: " + file_path)





# Usage example
json_file_path = "mix_scan.json"
interpret_json_file(json_file_path)







def window_name():
    print('window.name')

def chrome_meg():
    print('chrome_meg')

def window_hash():
    print('window_hash')


