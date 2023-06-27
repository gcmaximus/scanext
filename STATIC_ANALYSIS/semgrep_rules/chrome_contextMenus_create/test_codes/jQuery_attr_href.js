/*******************
chrome_contextMenus_create-jQuery_attr_href
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").attr("href", n.linkUrl); // Expect 1 match here
    $("f").attr("href", n.srcUrl); // Expect 1 match here
    $("f").attr("href", n.pageUrl); // Expect 1 match here
    $("f").attr("href", n.frameUrl); // Expect 1 match here
    $("f").attr("href", n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.srcUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.pageUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.frameUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.selectionText;
    $("f").attr("href", x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").attr("href", x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").attr("href", v);
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
            $("f").attr("href", v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").attr("href", x);

function aaa(n, a) {
    console.log();
    $("f").attr("href", n.linkUrl); // Expect 1 match here
    $("f").attr("href", n.srcUrl); // Expect 1 match here
    $("f").attr("href", n.pageUrl); // Expect 1 match here
    $("f").attr("href", n.frameUrl); // Expect 1 match here
    $("f").attr("href", n.selectionText); // Expect 1 match here

    $("f").attr("href", a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.srcUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.pageUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.frameUrl;
    $("f").attr("href", x); // Expect 1 match here

    x = n.selectionText;
    $("f").attr("href", x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").attr("href", v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").attr("href", n.linkUrl); // Expect 1 match here
            $("f").attr("href", n.srcUrl); // Expect 1 match here
            $("f").attr("href", n.pageUrl); // Expect 1 match here
            $("f").attr("href", n.frameUrl); // Expect 1 match here
            $("f").attr("href", n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.srcUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.pageUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.frameUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.selectionText;
            $("f").attr("href", x); // Expect 1 match here
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
            $("f").attr("href", v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").attr("href", n.linkUrl); // Expect 1 match here
            $("f").attr("href", n.srcUrl); // Expect 1 match here
            $("f").attr("href", n.pageUrl); // Expect 1 match here
            $("f").attr("href", n.frameUrl); // Expect 1 match here
            $("f").attr("href", n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.srcUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.pageUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.frameUrl;
            $("f").attr("href", x); // Expect 1 match here

            x = n.selectionText;
            $("f").attr("href", x); // Expect 1 match here
            console.log();

            $(x).attr("href", "f");
        },
        test2: "sdfs",
    },
    "adfs"
);
