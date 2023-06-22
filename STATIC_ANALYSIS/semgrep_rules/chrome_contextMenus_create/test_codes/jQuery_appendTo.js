/*******************
chrome_contextMenus_create-jQuery_appendTo
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").appendTo(n.linkUrl); // Expect 1 match here
    $("f").appendTo(n.srcUrl); // Expect 1 match here
    $("f").appendTo(n.pageUrl); // Expect 1 match here
    $("f").appendTo(n.frameUrl); // Expect 1 match here
    $("f").appendTo(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.selectionText;
    $("f").appendTo(x); // Expect 1 match here
    console.log();
}

let a = n.linkUrl;
$("f").appendTo(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").appendTo(v);
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
            $("f").appendTo(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").appendTo(x);

function aaa(n, a) {
    console.log();
    $("f").appendTo(n.linkUrl); // Expect 1 match here
    $("f").appendTo(n.srcUrl); // Expect 1 match here
    $("f").appendTo(n.pageUrl); // Expect 1 match here
    $("f").appendTo(n.frameUrl); // Expect 1 match here
    $("f").appendTo(n.selectionText); // Expect 1 match here

    $("f").appendTo(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").appendTo(x); // Expect 1 match here

    x = n.selectionText;
    $("f").appendTo(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").appendTo(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").appendTo(n.linkUrl); // Expect 1 match here
            $("f").appendTo(n.srcUrl); // Expect 1 match here
            $("f").appendTo(n.pageUrl); // Expect 1 match here
            $("f").appendTo(n.frameUrl); // Expect 1 match here
            $("f").appendTo(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.selectionText;
            $("f").appendTo(x); // Expect 1 match here
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
            $("f").appendTo(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").appendTo(n.linkUrl); // Expect 1 match here
            $("f").appendTo(n.srcUrl); // Expect 1 match here
            $("f").appendTo(n.pageUrl); // Expect 1 match here
            $("f").appendTo(n.frameUrl); // Expect 1 match here
            $("f").appendTo(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").appendTo(x); // Expect 1 match here

            x = n.selectionText;
            $("f").appendTo(x); // Expect 1 match here
            console.log();

            $(x).appendTo("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
