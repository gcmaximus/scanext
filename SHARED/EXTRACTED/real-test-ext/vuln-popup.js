console.log('this is the first line of the program')
// case 1
x = window.name
document.write(x)

// case 2
y = location.hash
console.log('hi')
tainted_y = y.split("#")[1]
console.log('bye')
very_tainted_y = tainted_y
console.log('hua')
console.log('hello')
damn_tainted_y = very_tainted_y + "===="
very_damn_tainted_y = damn_tainted_y
x = very_damn_tainted_y
console.log('uhud')
document.getElementById('abc').innerHTML = x

// case 3
console.log('bye')
document.writeln(location.href)

// case 4
x = location.search
console.log(x)
$('abc').html(x) // should be 0 intermediate vars, line diff > 1
console.log('this is the last line of the program')
