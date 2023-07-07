function vuln_func() {
    x = window.name
    console.log(x)
    tainted_x = x + 'abc'
    document.getElementById('replace').innerHTML = tainted_x
}

vuln_func()
