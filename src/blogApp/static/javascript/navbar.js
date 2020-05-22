const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");
const links = document.querySelectorAll(".nav-links li");
const navIcons = document.querySelector(".nav-icons");
const navLogin = document.querySelector(".nav-login");
const logo = document.querySelector(".logo");



hamburger.addEventListener("click", () =>{
  logo.classList.toggle("open");
  hamburger.classList.toggle("open");
  navLinks.classList.toggle("open");
  navLogin.classList.toggle("open");
  navIcons.classList.toggle("open");
  links.forEach(link =>{
    link.classList.toggle("fade");
  });
});
