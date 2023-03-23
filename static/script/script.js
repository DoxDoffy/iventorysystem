// darkmode:
let darkmode = document.querySelector('#darkmode');

darkmode.onclick = () => {
    if(darkmode.classList.contains('bx-moon')){
        darkmode.classList.replace('bx-moon', 'bx-sun');
        document.body.classList.add('color');
    }else{
        darkmode.classList.replace('bx-sun', 'bx-moon');
        document.body.classList.remove('color');
    }
};

// responsive nav bar- without this nav will not appear:
let menu = document.querySelector('#menu-icon');
let navlist =  document.querySelector('.navlist');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navlist.classList.toggle('open');
}

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navlist.classList.remove('open');
}

const sr = ScrollReveal({
    distance: '70px',
    duration: 2700,
    reset: true
});

sr.reveal('.hero-text , .sec2, .sec2-2',{delay:200,origin:'bottom'});
sr.reveal('.hero-img , .sec1, .sec2-btn',{delay:350,origin:'top'});


