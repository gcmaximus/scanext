/*******************
chrome_contextMenus_create-jQuery_insertBefore
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").insertBefore(n.linkUrl); // Expect 1 match here
    $("f").insertBefore(n.srcUrl); // Expect 1 match here
    $("f").insertBefore(n.pageUrl); // Expect 1 match here
    $("f").insertBefore(n.frameUrl); // Expect 1 match here
    $("f").insertBefore(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.selectionText;
    $("f").insertBefore(x); // Expect 1 match here
    console.log();
}

let a = n.linkUrl;
$("f").insertBefore(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertBefore(v);
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
            $("f").insertBefore(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").insertBefore(x);

function aaa(n, a) {
    console.log();
    $("f").insertBefore(n.linkUrl); // Expect 1 match here
    $("f").insertBefore(n.srcUrl); // Expect 1 match here
    $("f").insertBefore(n.pageUrl); // Expect 1 match here
    $("f").insertBefore(n.frameUrl); // Expect 1 match here
    $("f").insertBefore(n.selectionText); // Expect 1 match here

    $("f").insertBefore(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").insertBefore(x); // Expect 1 match here

    x = n.selectionText;
    $("f").insertBefore(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").insertBefore(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").insertBefore(n.linkUrl); // Expect 1 match here
            $("f").insertBefore(n.srcUrl); // Expect 1 match here
            $("f").insertBefore(n.pageUrl); // Expect 1 match here
            $("f").insertBefore(n.frameUrl); // Expect 1 match here
            $("f").insertBefore(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.selectionText;
            $("f").insertBefore(x); // Expect 1 match here
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
            $("f").insertBefore(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").insertBefore(n.linkUrl); // Expect 1 match here
            $("f").insertBefore(n.srcUrl); // Expect 1 match here
            $("f").insertBefore(n.pageUrl); // Expect 1 match here
            $("f").insertBefore(n.frameUrl); // Expect 1 match here
            $("f").insertBefore(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").insertBefore(x); // Expect 1 match here

            x = n.selectionText;
            $("f").insertBefore(x); // Expect 1 match here
            console.log();

            $(x).insertBefore("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
