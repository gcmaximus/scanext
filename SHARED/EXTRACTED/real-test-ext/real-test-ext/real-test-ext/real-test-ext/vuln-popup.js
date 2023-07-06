x = window.name

document.write(x)

y = location.hash

tainted_y = y.split("#")[1]

document.getElementById('abc').innerHTML = tainted_y

document.writeln(location.href)
