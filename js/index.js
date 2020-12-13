// javascript for index.html
const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

async function relocateSVG() {
    // console.log("Waiting for 5");
    await sleep(1000);
    svgs = document.getElementsByClassName("gh-button-svg");
    star = svgs[0];
    eye = svgs[1];
    fork = svgs[2];
    star.children[0].setAttribute("viewBox", "0 5 20 20");
    star.children[0].setAttribute("height", "28");
    star.children[0].setAttribute("width", "20");
    eye.children[0].setAttribute("viewBox", "0 5 20 20");
    eye.children[0].setAttribute("height", "28");
    eye.children[0].setAttribute("width", "20");
    fork.children[0].setAttribute("viewBox", "0 5 20 20");
    fork.children[0].setAttribute("height", "28");
    fork.children[0].setAttribute("width", "20");
    // fork.children[0].viewBox.baseVal.set
    // fork.children[0].viewBox.baseVal.height=20;
    // fork.children[0].viewBox.baseVal.width=5;
    // fork.children[0].height=28;
    // fork.children[0].width=20;
}


async function addIDs() {
    // console.log("Waiting for 5");
    await sleep(1000);
    btns = document.getElementsByClassName("gh-button-inside");
    star = btns[0];
    watch = btns[1];
    star.id = 'star';
    watch.id = 'watch';
}

relocateSVG();
addIDs();