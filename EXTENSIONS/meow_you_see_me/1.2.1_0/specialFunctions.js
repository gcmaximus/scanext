function specialFunction(cat) {
  switch (cat.name) {
    case "Unicorn Cat" :
      unicorn();
      break;
    case "Witch Cat" :
      witchSpecialFunction();
      break;
    case "Magic Cat" :
      teleport();
      break;
    case "Scaredy Cat" :
      scaredyCat();
      break;
  }
}

function specialCard(cat, catProfile) {
  switch (cat.name) {
    case "Unicorn Cat" :
      rainbowCard(catProfile);
      break;
    case "Witch Cat" :
      witchCard(catProfile);
      break;
    case "Cyber Cat" :
      cyberCard(catProfile);
      break;
    case "Reaper Cat" :
      reaperCard(catProfile);
      break;
    case "Flame Cat" :
      flameCard(catProfile);
      break;
  }
}

function unicorn() {
    let btn = document.getElementById('cat-btn');
  
    let body = document.body;
    let html = document.documentElement;
    let height = Math.max( body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight );
    let width = Math.max( body.scrollWidth, body.offsetWidth, html.clientWidth, html.scrollWidth, html.offsetWidth );
    
    let unicornSize = 30;
    let cushion = 3*unicornSize;
    let leftBound = cushion, rightBound = width - cushion;
    let bottomBound = height - cushion;
  
    btn.style.left = leftBound + 'px';
    btn.style.top = bottomBound + 'px';
  
    let numRevolutions = 3;
    // rise / run
    let slope = height / (width * 2 * numRevolutions);
  
    // pixels on x axis unicorn moves per second (not actual speed)
    let actualSpeed = 600;
    // let actualSpeed = 50;
    let speed = Math.cos(Math.atan(slope))*actualSpeed;
  
    let maxBounces = 14;
    let numberBounces = Math.min(maxBounces, height / (slope*width) );
  
    // seconds until unicorn starts
    let startTime = 0;
  
    let animationTime = width / speed * ( numberBounces + 1 );
    let endTime = startTime + animationTime;
  
  
    let horizontalMovement = rightBound - leftBound;
    let verticalMovement = horizontalMovement * slope;
  
    let unicornAnimationText = ' @keyframes unicorn { ';
    for (let i = 1; i < numberBounces + 1; i++) {
      percent = Math.round(i * 100 / numberBounces);
      unicornAnimationText += percent + '% { transform: translate(' + ( i % 2 === 0 ? 0 : horizontalMovement ) + 'px, ' + -i*verticalMovement + 'px) scale(100%); } ';
    }
    unicornAnimationText += '100% { transform: translate(0, -' + height + 'px) scale(0%); } } ';
  
    let style = document.getElementById('cat-style');
    let boxShadowSizing = '0 0 10px';
    style.innerText = style.innerText + 
    '#cat-btn, #cat-btn:hover { animation: unicorn ' + animationTime + 's linear; animation-fill-mode: forwards; }' +
    '#cat-btn img { animation: rainbow 1s infinite; }' + 
    unicornAnimationText + 
    '@keyframes rainbow { 0% { filter: drop-shadow(' + boxShadowSizing + ' red); } 20% { filter: drop-shadow(' + boxShadowSizing + ' yellow); } 40% { filter: drop-shadow(' + boxShadowSizing + ' green); } 60% { filter: drop-shadow(' + boxShadowSizing + ' blue); } 80% { filter: drop-shadow(' + boxShadowSizing + ' violet); } 100% { filter: drop-shadow(' + boxShadowSizing + ' red); } }' + 
    '@keyframes launch {0%, 100% {transform: none; opacity: 0;}}';

    let clickCushion = 2.5;
    document.addEventListener("click", (e) => {
      let btnRect = btn.getBoundingClientRect();
      let x = btnRect.left + (btnRect.right - btnRect.left) / 2;
      let y = btnRect.top + (btnRect.bottom - btnRect.top) / 2;
      if (Math.sqrt((x - e.clientX)**2 + (y - e.clientY)**2) < clickCushion*unicornSize / 2) {
        btn.click(e);
      }
    })
  
    setCatRemovalTimer(endTime);
  } // RAW "let t=document.getElementById('cat-btn');var e=document.body,n=document.documentElement,o=Math.max(e.scrollHeight,e.offsetHeight,n.clientHeight,n.scrollHeight,n.offsetHeight),r=Math.max(e.scrollWidth,e.offsetWidth,n.clientWidth,n.scrollWidth,n.offsetWidth),a=r-60,e=o-60;t.style.left='60px',t.style.top=e+'px';var n=o/(2*r*3),e=600*Math.cos(Math.atan(n)),i=Math.min(14,o/(n*r)),r=r/e*(i+1),e=0+r,l=a-60,s=l*n;let d=' @keyframes unicorn { ';for(let t=1;t<i+1;t++)percent=Math.round(100*t/i),d+=percent+'% { transform: translate('+(t%2==0?0:l)+'px, '+-t*s+'px) scale(100%); } ';d+='100% { transform: translate(0, -'+o+'px) scale(0%); } } ';let f=document.getElementById('cat-style');o='0 0 10px';f.innerText=f.innerText+'#cat-btn, #cat-btn:hover { animation: unicorn '+r+'s linear; animation-fill-mode: forwards; }#cat-btn img { animation: rainbow 1s infinite; }'+d+'@keyframes rainbow { 0% { filter: drop-shadow('+o+' red); } 20% { filter: drop-shadow('+o+' yellow); } 40% { filter: drop-shadow('+o+' green); } 60% { filter: drop-shadow('+o+' blue); } 80% { filter: drop-shadow('+o+' violet); } 100% { filter: drop-shadow('+o+' red); } }@keyframes launch {0% {transform: none;} 100% {transform:none;}}',setCatRemovalTimer(e)"

  
  function rainbowCard(catProfile) {
    catProfile.classList.add('unicorn');
    let style=document.createElement('style');
    style.innerText = '.unicorn img { animation: rainbow 2.5s infinite; } .unicorn:hover img {animation: rainbow 2.5s infinite, float 0.5s infinite } @keyframes rainbow { 0% { filter: drop-shadow(0 0 6px red); } 20% { filter: drop-shadow(0 0 6px yellow); } 40% { filter: drop-shadow(0 0 6px green); } 60% { filter: drop-shadow(0 0 6px blue); } 80% { filter: drop-shadow(0 0 6px violet); } 100% { filter: drop-shadow(0 0 6px red); } } .unicorn { background-image: linear-gradient(to left, violet, indigo, blue, green, orange, red); -webkit-background-clip: text; color: transparent; }';
    document.body.append(style);
} // RAW "catProfile.classList.add('unicorn');let e=document.createElement('style');e.innerText='.unicorn img{animation:rainbow 2.5s infinite;}.unicorn:hover img{animation:rainbow 2.5s infinite,float 0.5s infinite}@keyframes rainbow{0%{filter:drop-shadow(0 0 6px red);}20%{filter:drop-shadow(0 0 6px yellow);}40%{filter:drop-shadow(0 0 6px green);}60%{filter:drop-shadow(0 0 6px blue);}80%{filter:drop-shadow(0 0 6px violet);}100%{filter:drop-shadow(0 0 6px red);}}.unicorn{background-image:linear-gradient(to left,violet,indigo,blue,green,orange,red);-webkit-background-clip:text;color:transparent;}';document.body.append(e);"


function witchSpecialFunction() {
  let style = document.getElementById('cat-style');
  style.innerText = style.innerText + 
  '#cat-btn, #cat-btn:hover { filter: drop-shadow(0 0 6px green); animation: magic 4s infinite; }' + 
    '@keyframes magic { 0% { transform: translate(0,0); } 10% { transform: translate(15px,-5px); } 24% { transform: translate(10px, 5px); } 40% { transform: translate(20px,30px); } 75% { transform: translate(-20px,10px); } 90% { transform: translate(10px,-15px); } 100% { translate(0,0); } }';
} // RAW "let e=document.getElementById('cat-style');e.innerText=e.innerText+'#cat-btn,#cat-btn:hover{filter:drop-shadow(0 0 6px green);animation: magic 4s infinite;}@keyframes magic{0%{transform:translate(0,0);}10%{transform:translate(15px,-5px);}24%{transform:translate(10px,5px);}40%{transform:translate(20px,30px);}75%{transform:translate(-20px,10px);}90%{transform:translate(10px,-15px);}100%{translate(0,0);}}';"

function witchCard(catProfile) {
  catProfile.style = 'color: #00bb00;';
  [...catProfile.getElementsByTagName('img')][0].style='filter: drop-shadow(0 0 5px green);'
} // RAW "catProfile.style='color:#00bb00;';[...catProfile.getElementsByTagName('img')][0].style='filter:drop-shadow(0 0 5px green);'"

function teleport() {
  let style = document.getElementById('cat-style');
  style.innerText = style.innerText + '#cat-btn, #cat-btn:hover { animation: teleport 3s infinite; } @keyframes teleport { 0% { transform: scale(0%) rotate(180deg); } 10% { transform: scale(100%) rotate(0deg); } 90% { transform: scale(100%) rotate(0deg); } 100% { transform: scale(0%) rotate(180deg); } }';
  let btn = document.getElementById('cat-btn');
  btn.addEventListener('animationiteration', relocate);

  var body = document.body;
  var html = document.documentElement;
  var height = Math.max( body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight );
  var width = Math.max( body.scrollWidth, body.offsetWidth, html.clientWidth, html.scrollWidth, html.offsetWidth );
  function relocate() {
    btn.style.left = Math.floor(Math.random()*width) + 'px';
    btn.style.top = Math.floor(Math.random()*height) + 'px';
  }
} // RAW "let style=document.getElementById('cat-style');style.innerText=style.innerText+'#cat-btn, #cat-btn:hover { animation: teleport 3s infinite; } @keyframes teleport { 0% { transform: scale(0%) rotate(180deg); } 10% { transform: scale(100%) rotate(0deg); } 90% { transform: scale(100%) rotate(0deg); } 100% { transform: scale(0%) rotate(180deg); } }';let btn=document.getElementById('cat-btn');btn.addEventListener('animationiteration',relocate);var body=document.body,html=document.documentElement,height=Math.max(body.scrollHeight,body.offsetHeight,html.clientHeight,html.scrollHeight,html.offsetHeight),width=Math.max(body.scrollWidth,body.offsetWidth,html.clientWidth,html.scrollWidth,html.offsetWidth);function relocate(){btn.style.left=Math.floor(Math.random()*width)+'px',btn.style.top=Math.floor(Math.random()*height)+'px'}"

function scaredyCat() {
  let btn = document.getElementById('cat-btn');
  btn.style.animation = 'shake 0.1s infinite';
  let mouseArea = document.createElement('div');
  let img = [...btn.getElementsByTagName('img')][0];
  let style=document.getElementById('cat-style');
  let scareAreaSize = 150;
  let left = btn.style.left;
  btn.style.left = Number.parseInt(left.substr(0, left.indexOf('px'))) - 75 + 'px';
  let top = btn.style.top;
  btn.style.top = Number.parseInt(top.substr(0, top.indexOf('px'))) - 75 + 'px';
  mouseArea.style = `width:${scareAreaSize}px;height:${scareAreaSize}px;border-radius:50%;display:flex;justify-content:center;align-items:center;background:transparent;`;
  img.style = 'width:initial;margin:auto;';
  btn.append(mouseArea);
  mouseArea.append(img);
  style.innerText += '#cat-btn:hover{animation:none;} @keyframes shake {0%,100%{transform:rotate(-10deg);}50%{transform:rotate(10deg);}}';
  btn.addEventListener('mouseenter', actScared, {once: true});
  function actScared(e) {
    let btnLeft = btn.style.left;
    btnLeft  = btnLeft.substr(0, btnLeft.indexOf('px'));
    let btnTop = btn.style.top;
    btnTop  = btnTop.substr(0, btnTop.indexOf('px'));

    let btnX = Number.parseInt(btnLeft) + scareAreaSize*0.5;
    let btnY = Number.parseInt(btnTop) + scareAreaSize*0.5;

    let mouseX = e.pageX;
    let mouseY = e.pageY;
    let thet = Math.atan((btnY - mouseY) / (btnX - mouseX));
    if (btnX < mouseX) {
      thet -= Math.PI;
    }
    // pixels per second
    let speed = 300;

    // seconds
    let time = 3;
    btn.style.animation = `scaredyrun ${time}s forwards`;
    style.innerText += `@keyframes scaredyrun {0% {transform: translate(0,0);} 90% {transform:translate(${0.9*time*speed*Math.cos(thet)}px,${0.9*time*speed*Math.sin(thet)}px) scale(100%);} 100% {transform:translate(${time*speed*Math.cos(thet)}px,${time*speed*Math.sin(thet)}px) scale(0%);}}`;
    btn.addEventListener('animationend', () => {
      setTimeout(removeCatButton, 50);
    });
    btn.addEventListener('click', () => {
      setTimeout(removeCatButton, 50);
    });
  }
} // RAW "let btn=document.getElementById('cat-btn');btn.style.animation='shake 0.1s infinite';let mouseArea=document.createElement('div'),img=[...btn.getElementsByTagName('img')][0],style=document.getElementById('cat-style'),left=btn.style.left;btn.style.left=Number.parseInt(left.substr(0,left.indexOf('px')))-75+'px';let top=btn.style.top;function actScared(t){let e=btn.style.left;e=e.substr(0,e.indexOf('px'));let n=btn.style.top;n=n.substr(0,n.indexOf('px'));var a=Number.parseInt(e)+75,s=Number.parseInt(n)+75,r=t.pageX,t=t.pageY;let i=Math.atan((s-t)/(a-r));a<r&&(i-=Math.PI);btn.style.animation='scaredyrun 3s forwards',style.innerText+='@keyframes scaredyrun {0%{transform:translate(0,0);}90%{transform:translate('+810*Math.cos(i)+'px,'+810*Math.sin(i)+'px) scale(100%);}100%{transform:translate('+900*Math.cos(i)+'px,'+900*Math.sin(i)+'px) scale(0%);}}',btn.addEventListener('animationend',removeCatButton),btn.addEventListener('click',removeCatButton)}btn.style.top=Number.parseInt(top.substr(0,top.indexOf('px')))-75+'px',mouseArea.style='width:150px;height:150px;border-radius:50%;display:flex;justify-content:center;align-items:center;',img.style='width:initial;margin:auto;',btn.append(mouseArea),mouseArea.append(img),style.innerText+='#cat-btn:hover{animation:none;} @keyframes shake {0%,100%{transform:rotate(-10deg);}50%{transform:rotate(10deg);}}',btn.addEventListener('mouseenter',actScared,{once:!0});"

function cyberCard(catProfile) {
  catProfile.className = 'cyber';
  let style = document.createElement('style');
  let styleText = '';
  styleText += '.cyber {';
  styleText += 'background-image: linear-gradient(to top, #46d1d1, #dd55c5, #46d1d1, #46d1d1, #46d1d1);';
  styleText +=  '-webkit-background-clip: text;';
  styleText += 'color: transparent;';
  styleText += '}';
  styleText += '.cyber img{';
  styleText += 'filter: drop-shadow(0 0 4px #dd55c5) drop-shadow(0 0 5px #46d1d1);';
  styleText += '}';
  style.innerText = styleText;
  document.head.append(style);
} // RAW "catProfile.className='cyber';let e=document.createElement('style');e.innerText='.cyber{background-image:linear-gradient(to top,#46d1d1,#dd55c5,#46d1d1,#46d1d1,#46d1d1);-webkit-background-clip:text;color:transparent;}.cyber img{filter:drop-shadow(0 0 4px #dd55c5) drop-shadow(0 0 5px #46d1d1);}';document.head.append(e);"

function reaperCard(catProfile) {
  catProfile.style='filter:drop-shadow(0 0 2px black);color:black;';
} // RAW "catProfile.style='filter:drop-shadow(0 0 2px black);color:black;';"

function flameCard(catProfile) {
  catProfile.className = 'flame';
  let style = document.createElement('style');
  style.innerText = `
  .flame {
    color: #ff6800;
    filter: drop-shadow(0 0 4px #ff6800);
  }
  .flame img {
    filter: drop-shadow(0 0 2px orangered) drop-shadow(0 0 3px orange);
  }`
  document.head.append(style);
}