/*******************
chrome_contextMenus_update-jQuery_wrapInner
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").wrapInner(n.linkUrl); // Expect 1 match here
    $("f").wrapInner(n.srcUrl); // Expect 1 match here
    $("f").wrapInner(n.pageUrl); // Expect 1 match here
    $("f").wrapInner(n.frameUrl); // Expect 1 match here
    $("f").wrapInner(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").wrapInner(x);

chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapInner(v);
        },
        onclick: kms,
        test2: "sdfs",
    },
    "adfs"
);

// case 2
chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapInner(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").wrapInner(x);

function aaa(n, a) {
    console.log();
    $("f").wrapInner(n.linkUrl); // Expect 1 match here
    $("f").wrapInner(n.srcUrl); // Expect 1 match here
    $("f").wrapInner(n.pageUrl); // Expect 1 match here
    $("f").wrapInner(n.frameUrl); // Expect 1 match here
    $("f").wrapInner(n.selectionText); // Expect 1 match here

    $("f").wrapInner(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.update(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapInner(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").wrapInner(n.linkUrl); // Expect 1 match here
            $("f").wrapInner(n.srcUrl); // Expect 1 match here
            $("f").wrapInner(n.pageUrl); // Expect 1 match here
            $("f").wrapInner(n.frameUrl); // Expect 1 match here
            $("f").wrapInner(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.selectionText;
            $("f").wrapInner(x); // Expect 1 match here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);

// case 4
chrome.contextMenus.update(
    {
        ontest: function sss(n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").wrapInner(v);
        },
        onclick: function bbb(n, a) {
            console.log();
            $("f").wrapInner(n.linkUrl); // Expect 1 match here
            $("f").wrapInner(n.srcUrl); // Expect 1 match here
            $("f").wrapInner(n.pageUrl); // Expect 1 match here
            $("f").wrapInner(n.frameUrl); // Expect 1 match here
            $("f").wrapInner(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").wrapInner(x); // Expect 1 match here

            x = n.selectionText;
            $("f").wrapInner(x); // Expect 1 match here
            console.log();

            $(x).wrapInner("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
