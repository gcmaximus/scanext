console.log('first line of program')
y = "<div>pls no xss the report</div>"
console.log('nothing')
console.log('abc')

function abc() {
    x = "<h1>" + window.name + "</h1>"
    tainted_x = "<div>" + x + "</div>"
    document.getElementById('replace').outerHTML = tainted_x
}
console.log('last line bye bye')
z = "<img src=x>"
