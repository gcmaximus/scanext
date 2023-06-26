/*******************
chrome_contextMenus_create-setAttribute_src
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    document.getElementById("f").setAttribute("src", n.linkUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.srcUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.pageUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.frameUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.srcUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.pageUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.frameUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.selectionText; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here
    console.log();
}

let a = n.linkUrl;
document.getElementById("f").setAttribute("src", x);

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").setAttribute("src", v);
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
            document.getElementById("f").setAttribute("src", v);
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
document.getElementById("f").setAttribute("src", x);

function aaa(n, a) {
    console.log();
    document.getElementById("f").setAttribute("src", n.linkUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.srcUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.pageUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.frameUrl); // Expect 1 match here
    document.getElementById("f").setAttribute("src", n.selectionText); // Expect 1 match here

    document.getElementById("f").setAttribute("src", a.linkUrl);
    console.log();

    let x = n.linkUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.srcUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.pageUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.frameUrl; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here

    x = n.selectionText; 
    document.getElementById("f").setAttribute("src", x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").setAttribute("src", v);
        },
        onclick: function (n, a) {
            console.log();
            document.getElementById("f").setAttribute("src", n.linkUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.srcUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.pageUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.frameUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.srcUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.pageUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.frameUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.selectionText;
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here
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
            document.getElementById("f").setAttribute("src", v);
        },
        onclick: function kms(n, a) {
            console.log();
            document.getElementById("f").setAttribute("src", n.linkUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.srcUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.pageUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.frameUrl); // Expect 1 match here
            document.getElementById("f").setAttribute("src", n.selectionText); // Expect 1 match here
            console.log();

            let x = n.linkUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.srcUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.pageUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.frameUrl; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here

            x = n.selectionText; 
            document.getElementById("f").setAttribute("src", x); // Expect 1 match here
            console.log();
            
            document.getElementById(x).setAttribute("src", 'a')
        },
        test2: "sdfs",
    },
    "adfs"
);
