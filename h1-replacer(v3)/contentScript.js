console.log('line')
var v = window.name
// var s = `<img src=x onerror=${v}>`
// document.write(s)
var tags = document.getElementsByTagName('h1')

for (let i=0; i<tags.length; i++) {
    tags[i].innerHTML = v
}



// var replacementInput = document.getElementById('replacementInput');
// var tags = document.getElementsByTagName('h1')

// semgrep test
// var a = window.name
// document.getElementById('id').outerHTML = a
