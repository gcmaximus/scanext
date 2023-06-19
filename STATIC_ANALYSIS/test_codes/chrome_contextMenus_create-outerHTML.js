/*******************
chrome_contextMenus_create-outerHTML
*******************/


// Expected total matches: 40


// case 1
function kms(n, a) {
    console.log();
    document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here

    console.log();

    let x = n.linkUrl; // Expect 1 match here ...
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.selectionText; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    console.log();
}

let a = n.linkUrl;
document.getElementById("f").outerHTML = x;

chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").outerHTML = v;
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
            document.getElementById("f").outerHTML = v;
        },
        onclick: aaa,
        test2: "sdfs",
    },
    "adfs"
);

let b = n.linkUrl;
document.getElementById("f").outerHTML = x;

function aaa(n, a) {
    console.log();
    document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here

    console.log();

    let x = n.linkUrl; // Expect 1 match here ...
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    
    x = n.selectionText; // Expect 1 match here
    document.getElementById("f").outerHTML = x; // ... end here
    console.log();
}


// case 3
chrome.contextMenus.create(
    {
        ontest: function (n, a) {
            let x = n.linkUrl;
            let v = x;
            document.getElementById("f").outerHTML = v;
        },
        onclick: function (n, a) {
            console.log();
            document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here
            console.log();

            let x = n.linkUrl; // Expect 1 match here ...
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.srcUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.pageUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.frameUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.selectionText; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
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
            document.getElementById("f").outerHTML = v;
        },
        onclick: function kms(n, a) {
            console.log();
            document.getElementById("f").outerHTML = n.linkUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.srcUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.pageUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.frameUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = n.selectionText; // Expect 1 match here
            console.log();

            let x = n.linkUrl; // Expect 1 match here ...
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.srcUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.pageUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.frameUrl; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
            
            x = n.selectionText; // Expect 1 match here
            document.getElementById("f").outerHTML = x; // ... end here
            console.log();
        },
        test2: "sdfs",
    },
    "adfs"
);
