/*******************
chrome_contextMenus_create-jQuery_html
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").html(n.linkUrl); // Expect 1 match here
    $("f").html(n.srcUrl); // Expect 1 match here
    $("f").html(n.pageUrl); // Expect 1 match here
    $("f").html(n.frameUrl); // Expect 1 match here
    $("f").html(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").html(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").html(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").html(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").html(x); // Expect 1 match here

    x = n.selectionText;
    $("f").html(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").html(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").html(v);
        },
        onclick: kms,
        test2: "sdfs",
    },
    "adfs"
);

// case 2
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").html(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").html(x);

function aaa(n, a) {
    console.log();
    $("f").html(n.linkUrl); // Expect 1 match here
    $("f").html(n.srcUrl); // Expect 1 match here
    $("f").html(n.pageUrl); // Expect 1 match here
    $("f").html(n.frameUrl); // Expect 1 match here
    $("f").html(n.selectionText); // Expect 1 match here

    $("f").html(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").html(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").html(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").html(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").html(x); // Expect 1 match here

    x = n.selectionText;
    $("f").html(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").html(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").html(n.linkUrl); // Expect 1 match here
            $("f").html(n.srcUrl); // Expect 1 match here
            $("f").html(n.pageUrl); // Expect 1 match here
            $("f").html(n.frameUrl); // Expect 1 match here
            $("f").html(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").html(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").html(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").html(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").html(x); // Expect 1 match here

            x = n.selectionText;
            $("f").html(x); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);

// case 4
chrome.contextMenus.create(
    {
        ontest: function sss(n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").html(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").html(n.linkUrl); // Expect 1 match here
            $("f").html(n.srcUrl); // Expect 1 match here
            $("f").html(n.pageUrl); // Expect 1 match here
            $("f").html(n.frameUrl); // Expect 1 match here
            $("f").html(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").html(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").html(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").html(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").html(x); // Expect 1 match here

            x = n.selectionText;
            $("f").html(x); // Expect 1 match here
            console.log();

            $(x).html("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
