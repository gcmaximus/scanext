$("button").click(function() {
    var vuln = location.href
    var useless = "useless"
    var vuln2 = vuln + useless

    $(`<p>This is your href: <span>${vuln2}</span></p>`).prependTo("div");
})