import re

# Sample JavaScript code
javascript_code = '''
window.addEventListener('message', function(event) {
    var data = event.data;
    
    var string1 = data.test1;
    var modifiedData = preprocess(test2);
    var string2 = modifiedData.test3;
    var string3 = data.test4;
    var string4 = event.data.test5
    var string5 = event.data.test6
    var string6 = event.data['test7']
    var string = event.data["test8"]

    var string6 = event.data[fake]

    


});
'''

# Regular expression patterns to match event.data.(string)
patterns = [
    r'event\.data\["(\w+)"\]',  # Matches event.data["field"]
    r"event\.data\['(\w+)'\]",  # Matches event.data['field']
    r'event\.data\.(\w+)',       # Matches event.data.field


    r'event\.data(?:[^.]|\.(?!\w))*\.(\w+)' # Matches nested

]


# Extract the strings using regex with multiline flag
matches = []
for pattern in patterns:
    matches.extend(re.findall(pattern, javascript_code, re.MULTILINE))

# Print the extracted strings
print(matches)






# pattern = r'event\.data(?:[^.]|\.(?!\w))*\.(\w+)'
