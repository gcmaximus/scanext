// testedon http://example.com

function handleAppend() {
    var caseAppend = window.name;
    var element = document.createElement("div");
    element.textContent = caseAppend;
    document.body.appendChild(element);
  }
  
  function handleInnerHTML() {
    var caseInnerHTML = window.name;
    var element = document.getElementsByTagName[0]
    console.log(element)
    element.innerHTML = caseInnerHTML;
  }
  
  function handleSetAttribute() {
    var caseSetAttribute = window.name;
    var linkElement = document.getElementById("targetLink");
    linkElement.setAttribute("href", caseSetAttribute);
  }
  
  handleAppend();
  handleInnerHTML();
  handleSetAttribute();