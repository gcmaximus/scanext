/*******************
chrome_cookies_getAll-chrome_tabs_update
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();

    let rite11 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(a, rite11, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update(a, { abc: "", url: n.value, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match

    let rite12 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite12);

    let rite13 = { abc: "", url: n.value, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite13, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update({ abc: "", url: n.name, cdb: "sdf" }); // Expect 1 match

    console.log();

    let x = n.name;
    let rite14 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(a, rite14, (tab) => {
        console.log(tab);
    });

    x = n.value;
    chrome.tabs.update(a, { abc: "", url: x, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match here

    x = n.name;
    let rite15 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite15);

    x = n.value;
    let rite16 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite16, (tab) => {
        console.log(tab);
    });

    x = n.name;
    chrome.tabs.update({ abc: "", url: x, cdb: "sdf" }); // Expect 1 match here
    console.log();
}

let n = { name: "" };
let a = n.name;
chrome.tabs.update({ abc: "", url: a, cdb: "sdf" }); // err

chrome.cookies.getAll({ name: "" }, kms);

// case 2
chrome.cookies.getAll({ name: "" }, aaa);

let b = n.name;
chrome.tabs.update({ abc: "", url: b, cdb: "sdf" }); // err

function aaa(n, a) {
    console.log();

    let rite21 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(a, rite21, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update(a, { abc: "", url: n.value, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match

    let rite22 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite22);

    let rite23 = { abc: "", url: n.value, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite23, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update({ abc: "", url: n.name, cdb: "sdf" }); // Expect 1 match

    console.log();

    let x = n.name;
    let rite24 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(a, rite24, (tab) => {
        console.log(tab);
    });

    x = n.value;
    chrome.tabs.update(a, { abc: "", url: x, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match here

    x = n.name;
    let rite25 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite25);

    x = n.value;
    let rite26 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite26, (tab) => {
        console.log(tab);
    });

    x = n.name;
    chrome.tabs.update({ abc: "", url: x, cdb: "sdf" }); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.getAll({ name: "" }, function (n, a) {
    console.log();
    let rite31 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(a, rite31, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update(a, { abc: "", url: n.value, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match

    let rite32 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite32);

    let rite33 = { abc: "", url: n.value, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite33, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update({ abc: "", url: n.name, cdb: "sdf" }); // Expect 1 match

    console.log();

    let x = n.name;
    let rite34 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(a, rite34, (tab) => {
        console.log(tab);
    });

    x = n.value;
    chrome.tabs.update(a, { abc: "", url: x, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match here

    x = n.name;
    let rite35 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite35);

    x = n.value;
    let rite36 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite36, (tab) => {
        console.log(tab);
    });

    x = n.name;
    chrome.tabs.update({ abc: "", url: x, cdb: "sdf" }); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.getAll({ name: "" }, function bbb(n, a) {
    console.log();
    let rite41 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(a, rite41, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update(a, { abc: "", url: n.value, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match

    let rite42 = { abc: "", url: n.name, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite42);

    let rite43 = { abc: "", url: n.value, cdb: "sdf" }; // Expect 1 match
    chrome.tabs.update(rite43, (tab) => {
        console.log(tab);
    });

    chrome.tabs.update({ abc: "", url: n.name, cdb: "sdf" }); // Expect 1 match

    console.log();

    let x = n.name;
    let rite44 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(a, rite44, (tab) => {
        console.log(tab);
    });

    x = n.value;
    chrome.tabs.update(a, { abc: "", url: x, cdb: "sdf" }, (tab) => {
        console.log(tab);
    }); // Expect 1 match here

    x = n.name;
    let rite45 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite45);

    x = n.value;
    let rite46 = { abc: "", url: x, cdb: "sdf" }; // Expect 1 match here
    chrome.tabs.update(rite46, (tab) => {
        console.log(tab);
    });

    x = n.name;
    chrome.tabs.update({ abc: "", url: x, cdb: "sdf" }); // Expect 1 match here
    console.log();
});
