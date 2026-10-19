const giftCardForm = document.querySelector('#giftcardForm')

giftCardForm?.addEventListener("submit", async (event) => {

    event.preventDefault()

    const giftInput = document.querySelector("#giftcode")
    if (giftInput.value.length < 4) return;

    const giftCardCTA = document.querySelector("[data-giftcard-state]")
    giftCardCTA.setAttribute("data-giftcard-state", "loading")

    const stage1 = document.querySelector("#giftcard__response--stage1")
    const stage2 = document.querySelector("#giftcard__response--stage2")

    try {
        const giftCardFormData = new FormData(giftCardForm);
        const { data } = await axios.post("/#giftcardbalance", giftCardFormData)
        const parser = new DOMParser;
        const giftCardDOM = parser.parseFromString(data, "text/html");
        const giftCardStatusMessage = document.querySelector("#status-giftcard")

        const giftCardResponse = giftCardDOM.querySelector("#rezultatGiftCard p").textContent.trim()
        giftCardStatusMessage.textContent = giftCardResponse

        setTimeout(() => {
            stage1.style.display = "none"
            stage2.style.display = "block"
            giftInput.value = ""
            giftCardCTA.setAttribute("data-giftcard-state", "idle")
        }, 1000)

    } catch (error) {
        console.log(error)
    }
    const backCTA = document.querySelector(".giftcard__back--btn")

    backCTA.addEventListener("click", () => {
        stage2.style.display = "none"
        stage1.style.display = "block"
    })
})