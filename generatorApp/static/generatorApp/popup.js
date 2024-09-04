const popup = document.getElementById("popup");
const logout = document.getElementById("logout");
const logoutForm = document.getElementById("logout-form")

logout.addEventListener('click', () => {
    popup.style.display = "flex"
})

popup.addEventListener('click', () => {
    popup.style.display = "none"
})