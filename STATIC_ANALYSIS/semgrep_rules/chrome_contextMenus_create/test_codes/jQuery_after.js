/*******************
chrome_contextMenus_create-jQuery_after
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").after(n.linkUrl); // Expect 1 match here
    $("f").after(n.srcUrl); // Expect 1 match here
    $("f").after(n.pageUrl); // Expect 1 match here
    $("f").after(n.frameUrl); // Expect 1 match here
    $("f").after(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").after(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").after(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").after(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").after(x); // Expect 1 match here

    x = n.selectionText;
    $("f").after(x); // Expect 1 match here
    console.log();
}

let a = n.linkUrl;
$("f").after(x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").after(v);
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
            $("f").after(v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
$("f").after(x);

function aaa(n, a) {
    console.log();
    $("f").after(n.linkUrl); // Expect 1 match here
    $("f").after(n.srcUrl); // Expect 1 match here
    $("f").after(n.pageUrl); // Expect 1 match here
    $("f").after(n.frameUrl); // Expect 1 match here
    $("f").after(n.selectionText); // Expect 1 match here

    $("f").after(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").after(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").after(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").after(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").after(x); // Expect 1 match here

    x = n.selectionText;
    $("f").after(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            $("f").after(v);
        },
        onclick: function (n, a) {
            console.log();
            $("f").after(n.linkUrl); // Expect 1 match here
            $("f").after(n.srcUrl); // Expect 1 match here
            $("f").after(n.pageUrl); // Expect 1 match here
            $("f").after(n.frameUrl); // Expect 1 match here
            $("f").after(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").after(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").after(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").after(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").after(x); // Expect 1 match here

            x = n.selectionText;
            $("f").after(x); // Expect 1 match here
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
            $("f").after(v);
        },
        onclick: function kms(n, a) {
            console.log();
            $("f").after(n.linkUrl); // Expect 1 match here
            $("f").after(n.srcUrl); // Expect 1 match here
            $("f").after(n.pageUrl); // Expect 1 match here
            $("f").after(n.frameUrl); // Expect 1 match here
            $("f").after(n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl;
            $("f").after(x); // Expect 1 match here

            x = n.srcUrl;
            $("f").after(x); // Expect 1 match here

            x = n.pageUrl;
            $("f").after(x); // Expect 1 match here

            x = n.frameUrl;
            $("f").after(x); // Expect 1 match here

            x = n.selectionText;
            $("f").after(x); // Expect 1 match here
            console.log();

            $(x).after("f");
        },
        test2: "sdfs",
    },
    "adfs"
);
