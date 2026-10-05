
document.querySelectorAll("[data-year]").forEach(el => {
  el.textContent = new Date().getFullYear();
});
const button = document.querySelector(".menu");
const nav = document.querySelector(".nav-links");
if(button && nav){
  button.addEventListener("click", () => nav.classList.toggle("open"));
}
