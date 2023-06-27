/*******************
chrome_contextMenus_create-jQuery_prepend
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").prepend(n.linkUrl); // Expect 1 match here
    $("f").prepend(n.srcUrl); // Expect 1 match here
    $("f").prepend(n.pageUrl); // Expect 1 match here
    $("f").prepend(n.frameUrl); // Expect 1 match here
    $("f").prepend(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.selectionText;
    $("f").prepend(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").prepend(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").prepend(v);
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
            $("f").prepend(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").prepend(x);

function aaa(n, a) {
    console.log();
    $("f").prepend(n.linkUrl); // Expect 1 match here
    $("f").prepend(n.srcUrl); // Expect 1 match here
    $("f").prepend(n.pageUrl); // Expect 1 match here
    $("f").prepend(n.frameUrl); // Expect 1 match here
    $("f").prepend(n.selectionText); // Expect 1 match here

    $("f").prepend(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.selectionText;
    $("f").prepend(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").prepend(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").prepend(n.linkUrl); // Expect 1 match here
            $("f").prepend(n.srcUrl); // Expect 1 match here
            $("f").prepend(n.pageUrl); // Expect 1 match here
            $("f").prepend(n.frameUrl); // Expect 1 match here
            $("f").prepend(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.selectionText;
            $("f").prepend(x); // Expect 1 match here
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
            $("f").prepend(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").prepend(n.linkUrl); // Expect 1 match here
            $("f").prepend(n.srcUrl); // Expect 1 match here
            $("f").prepend(n.pageUrl); // Expect 1 match here
            $("f").prepend(n.frameUrl); // Expect 1 match here
            $("f").prepend(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").prepend(x); // Expect 1 match here

            x = n.selectionText;
            $("f").prepend(x); // Expect 1 match here
            console.log();

            $(x).prepend("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
