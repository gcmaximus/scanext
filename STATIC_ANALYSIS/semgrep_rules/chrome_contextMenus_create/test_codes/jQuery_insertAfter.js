/*******************
chrome_contextMenus_create-jQuery_insertAfter
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").insertAfter(n.linkUrl); // Expect 1 match here
    $("f").insertAfter(n.srcUrl); // Expect 1 match here
    $("f").insertAfter(n.pageUrl); // Expect 1 match here
    $("f").insertAfter(n.frameUrl); // Expect 1 match here
    $("f").insertAfter(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.selectionText;
    $("f").insertAfter(x); // Expect 1 match here
    console.log();
}

let a = n.linkUrl;
$("f").insertAfter(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertAfter(v);
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
            $("f").insertAfter(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").insertAfter(x);

function aaa(n, a) {
    console.log();
    $("f").insertAfter(n.linkUrl); // Expect 1 match here
    $("f").insertAfter(n.srcUrl); // Expect 1 match here
    $("f").insertAfter(n.pageUrl); // Expect 1 match here
    $("f").insertAfter(n.frameUrl); // Expect 1 match here
    $("f").insertAfter(n.selectionText); // Expect 1 match here

    $("f").insertAfter(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").insertAfter(x); // Expect 1 match here

    x = n.selectionText;
    $("f").insertAfter(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertAfter(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").insertAfter(n.linkUrl); // Expect 1 match here
            $("f").insertAfter(n.srcUrl); // Expect 1 match here
            $("f").insertAfter(n.pageUrl); // Expect 1 match here
            $("f").insertAfter(n.frameUrl); // Expect 1 match here
            $("f").insertAfter(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.selectionText;
            $("f").insertAfter(x); // Expect 1 match here
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
            $("f").insertAfter(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").insertAfter(n.linkUrl); // Expect 1 match here
            $("f").insertAfter(n.srcUrl); // Expect 1 match here
            $("f").insertAfter(n.pageUrl); // Expect 1 match here
            $("f").insertAfter(n.frameUrl); // Expect 1 match here
            $("f").insertAfter(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").insertAfter(x); // Expect 1 match here

            x = n.selectionText;
            $("f").insertAfter(x); // Expect 1 match here
            console.log();

            $(x).insertAfter("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
