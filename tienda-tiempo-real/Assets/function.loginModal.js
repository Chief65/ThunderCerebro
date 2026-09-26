// heck if steam is enabled, if is not the avatar will change while typing in the input from login modal

{% if config("serverType") == "Minecraft" %}
document.querySelector("#mc_IGN_INPUT").addEventListener("keyup", function (e) {
    if (this.value.length > 1) {

        let skin = this.value

        if (skin[0] === '{{ config("bedrockPrefix") }}') {
            skin = skin.slice(1)
        }

        document.querySelector("#avatar_MC").src = `https://minotar.net/avatar/${skin}/32`

        return
    }
    document.querySelector("#avatar_MC").src = `https://minotar.net/avatar/MHF_Question/32`
})

{% endif %}

const clickableCategories = document.querySelectorAll("[data-login-category]")
let lastClickedCategoryLink

clickableCategories?.forEach(category => {
    category.addEventListener("click", function (e) {
        e.preventDefault()
        lastClickedCategoryLink = e.target.getAttribute("href")
        closeModal()
    })
});

const bedrockUser = document.querySelector("#bedrockIGN")

const loginForm = document.querySelector(".login-panel form")

loginForm.addEventListener("submit", async function (e) {

    e.preventDefault()
    const username = document.querySelector("#mc_IGN_INPUT")

    if (username.value.length < 3) {
        username.classList.add("login-error")
        return
    }

    if (bedrockUser?.checked && username.value[0] !== `{{ config("bedrockPrefix") }}`) {
        username.value = `{{ config("bedrockPrefix") }}${username.value}`
    }

    const loginLoader = document.querySelector(".login-loader")
    const successAnimation = document.querySelector("#successAnimation")
    const loadingAnimated = document.querySelector(".loading__animated")

    loginLoader.style.display = "flex"
    username.classList.remove("login-error")

    const response = await fetch("/login", {
        method: "POST",
        body: new FormData(this)
    })

    const { status } = await response

    if (status === 200) {

        setTimeout(() => {

            loadingAnimated.style.display = "none"
            successAnimation.style.display = "block"

            if (lastClickedCategoryLink) {
                window.location = lastClickedCategoryLink
                return
            }

            location.reload()

        }, 1000);

    }

})
