console.log('line')
var v = window.name
var s = `<img src=x onerror=${v}>`
// document.write(s)
document.write(v)
var replacementInput = document.getElementById('replacementInput');
var tags = document.getElementsByTagName('h1')

// semgrep test
var a = window.name
document.getElementById('id').outerHTML = a
