/*******************
chrome_cookies_getAll-jQuery_appendTo
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).appendTo("f"); // Expect 1 match here
    $(n.srcUrl).appendTo("f"); // Expect 1 match here
    $(n.pageUrl).appendTo("f"); // Expect 1 match here
    $(n.frameUrl).appendTo("f"); // Expect 1 match here
    $(n.selectionText).appendTo("f"); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$(x).appendTo("f");

chrome.cookies.getAll({ name: "" }, kms);

// case 2
chrome.cookies.getAll({ name: "" }, aaa);

let b = n.linkUrl;
$(x).appendTo("f");

function aaa(n, a) {
    console.log();
    $(n.linkUrl).appendTo("f"); // Expect 1 match here
    $(n.srcUrl).appendTo("f"); // Expect 1 match here
    $(n.pageUrl).appendTo("f"); // Expect 1 match here
    $(n.frameUrl).appendTo("f"); // Expect 1 match here
    $(n.selectionText).appendTo("f"); // Expect 1 match here

    $("f").appendTo(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.getAll({ name: "" }, function (n, a) {
    console.log();
    $(n.linkUrl).appendTo("f"); // Expect 1 match here
    $(n.srcUrl).appendTo("f"); // Expect 1 match here
    $(n.pageUrl).appendTo("f"); // Expect 1 match here
    $(n.frameUrl).appendTo("f"); // Expect 1 match here
    $(n.selectionText).appendTo("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.getAll({ name: "" }, function bbb(n, a) {
    console.log();
    $(n.linkUrl).appendTo("f"); // Expect 1 match here
    $(n.srcUrl).appendTo("f"); // Expect 1 match here
    $(n.pageUrl).appendTo("f"); // Expect 1 match here
    $(n.frameUrl).appendTo("f"); // Expect 1 match here
    $(n.selectionText).appendTo("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
});
