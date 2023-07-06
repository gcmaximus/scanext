// case 1
x = window.name
document.write(x)

// case 2
y = location.hash
console.log('hi')
tainted_y = y.split("#")[1]
very_tainted_y = tainted_y
document.getElementById('abc').innerHTML = very_tainted_y

// case 3
console.log('bye')
document.writeln(location.href)

// case 4
x = location.search
console.log(x)
$('abc').html(x) // should be 0 intermediate vars, line diff > 1
