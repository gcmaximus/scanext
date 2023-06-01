var gh = window.name

function pop(a) {

  document.getElementById('displayArea').innerHTML = a;
  document.getElementById('displayArea').outerHTML = a;
}

pop(window.name)