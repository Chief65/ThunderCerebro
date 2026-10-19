$("#activate-dropdown").click(function () {
    $("#dropdown-currency-triplezone").slideToggle(100, "linear");
});

$(".cart__review").click(function () {
    $(".cart__action--compress i").toggleClass("rotate__compress")
    $(".cart__items").toggle()
})

const accordions = document.querySelectorAll("[data-type='accordion']");
const defaultOpenedAccordions = document.querySelectorAll('[data-accordion="true"]')

defaultOpenedAccordions?.forEach(function (accordion) {
    const accordionContent = accordion.querySelector(".accordion__panel")
    accordionContent.style.maxHeight = accordionContent.scrollHeight + "px";
})

accordions?.forEach(accordion => {
    accordion?.addEventListener("click", function () {

        const parent = this.parentElement
        const isAccordionActive = parent.getAttribute("data-accordion") == "true"
        const accordionContent = this.nextElementSibling

        if (isAccordionActive) {
            accordionContent.style.maxHeight = null;
            parent.setAttribute("data-accordion", false)
            return
        }

        accordionContent.style.maxHeight = accordionContent.scrollHeight + "px";
        parent.setAttribute("data-accordion", true)
    })
})

const countdowns = document.querySelectorAll(".countdown-to")
countdowns.forEach(countdown => {
    setInterval(() => {
        let timeLeft = parseInt(countdown.getAttribute("data-countdown"))

        if (timeLeft === 0) {
            countdown.textContent = "Time Expired!"
            return
        }

        timeLeft--
        countdown.setAttribute("data-countdown", timeLeft)

        const days = Math.floor(timeLeft / (60 * 60 * 24));
        const hours = Math.floor((timeLeft % (60 * 60 * 24)) / (60 * 60));
        const minutes = Math.floor((timeLeft % (60 * 60)) / (60));
        const seconds = Math.floor((timeLeft % 60));

        countdown.textContent = `${days}D ${hours}H ${minutes}M ${seconds}S`

    }, 1000)
})

try {
    let placeholderGiftcard = document.querySelector(".__input--options")
    if (placeholderGiftcard.placeholder == "Please enter the email address this giftcard should be sent to") {
        placeholderGiftcard.setAttribute("placeholder", "{{ lang.giftcard_mail }}")
    }
    const paragraphs = document.querySelectorAll("p")

    paragraphs.forEach((pa) => {
        if (pa.textContent === "Login with Discord so that we can identify you")
            pa.textContent = "{{ lang.loginWithDiscord }}"
    })
} catch (error) {
    console.log("Not login page")
}