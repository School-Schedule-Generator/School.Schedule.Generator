const navbar = document.querySelector(".nav");
window.addEventListener("scroll", () => {
    if (window.scrollY > 20) {
        navbar.classList.add("nav-scrolled");
        navbar.classList.remove("nav-top");
    } else {
        navbar.classList.add("nav-top");
        navbar.classList.remove("nav-scrolled");
    }
});
