console.log('line')
var s = `<img src=x onerror=alert(1)>`
document.write(s)
var replacementInput = document.getElementById('replacementInput');
var tags = document.getElementsByTagName('h1')

// semgrep test
var a = window.name
document.getElementById('id').outerHTML = a
