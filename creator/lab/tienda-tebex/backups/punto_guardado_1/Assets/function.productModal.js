const packageModalButtons = document.querySelectorAll(".triplezone__toogle--modal")
const closeModalButtons = document.querySelectorAll(".modal__content--close")
const packageModal = document.querySelector("[data-modal-type='package']")
const modalContent = document.querySelector('.modal__content__box')
const bodyElement = document.querySelector("body")

const modals = document.querySelectorAll("[data-modal-type]")
const modalButtons = document.querySelectorAll("[data-modal-toggler]")

// Normal Modal
modalButtons?.forEach(button => {
    button?.addEventListener("click", (e) => {

        e.preventDefault()

        const modalType = button.getAttribute("data-modal-toggler")
        const modal = document.querySelector(`[data-modal-type='${modalType}']`)

        modal.showModal()
        removeLoadingModal()

    })
})

// Product Modal
packageModalButtons.forEach(button => {
    button?.addEventListener("click", async (e) => {

        e.preventDefault()
        const removePackage = button.getAttribute("data-remote")

        try {
            packageModal.showModal()
            bodyElement.setAttribute('data-modal-opened', '')

            const response = await fetch(removePackage)
            const parser = new DOMParser;

            if (response.ok) {

                removeLoadingModal()

                const data = await response.text()
                const dataModalHTML = parser.parseFromString(data, "text/html");

                modalContent.innerHTML = new XMLSerializer().serializeToString(dataModalHTML)
                
                {% include 'sliderAddon.js' ignore missing %}

                const giftButton = document.querySelector('[data-type-cta="gift"]')
                giftButton?.addEventListener("click", toggleGiftForm)
                
                // Close the modal if the user is not logged in
                document.querySelectorAll("[data-cart-modal-login]").forEach(button => {
                    button.addEventListener("click", (e) => {
                        e.preventDefault()
                        closeModal()
                        $("#modal-login").iziModal("open")
                    })
                })

            } else {
                closeModal()
            }

        } catch (error) {
            console.log(error);
            closeModal()
        }

    })
})

document.addEventListener("keydown", (e) => {

    const areModalsOpened = [...modals].some(modal => modal.open)
    const isModalOpenedAndEscPressed = e.key === "Escape" && areModalsOpened

    if (isModalOpenedAndEscPressed) {
        closeModal()
    }

})

modals?.forEach(modal => {
    modal?.addEventListener("click", onClickOutside);
})

closeModalButtons?.forEach(btn => {
    btn?.addEventListener("click", closeModal);
})

function toggleGiftForm() {
    const giftForm = document.querySelector(".package__modal__side__header__content__actions__gift")

    document.querySelector('[data-type-cta="gift"]')?.toggleAttribute("data-gift-active")
    const isGiftFormActive = giftForm.hasAttribute("data-giftform-active")

    giftForm?.toggleAttribute("data-giftform-active")

    if (isGiftFormActive) {
        giftForm.style.maxHeight = null;
        return
    }

    giftForm.style.maxHeight = giftForm.scrollHeight + "px";

}

function removeLoadingModal() {
    modals?.forEach(modal => {
        if (modal.open) {
            modal.removeAttribute("data-loading-modal")
        }
    })
}

function closeModal() {

    modals.forEach(modal => {

        if (modal.open) {
            modal.setAttribute("closing", "");
            modal.addEventListener("animationend", () => {
                modal.removeAttribute("closing");
                modal.close();
                bodyElement.removeAttribute('data-modal-opened')
                modal.setAttribute("data-loading-modal", '')
            }, { once: true })
        }

    })

}

function onClickOutside(event) {

    modals.forEach(modal => {
        if (event.target === modal) {
            closeModal();
        }
    })

}