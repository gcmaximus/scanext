/*******************
  1. window.name  
*******************/ 
// innerHTML
// case 1
var case1 = window.name
document.getElementById('case1').innerHTML = case1

// case 2
document.getElementById('case2').innerHTML = window.name

// case 3
var case3 = window.name
newcase3 = case3 + " "
document.getElementById('case3').innerHTML = newcase3

//outerHTML
// case 4
var case4 = window.name
document.getElementById('case4').innerHTML = case4

// case 5
document.getElementById('case5').innerHTML = window.name

// case 6
var case6 = window.name
newcase6 = case6 + " "
document.getElementById('case6').innerHTML = newcase6

/*******************
  2. location.hash  
*******************/ 

