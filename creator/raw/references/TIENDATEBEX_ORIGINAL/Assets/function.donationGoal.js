{% if page.title == "Welcome" %}
try {
    const goalProgress = document.querySelector(".splash__goal__footer--progress")
    const goalProgressText = document.querySelector("[data-goal-progress]")
    const goalAmount = document.querySelector("[data-goal-amount]")

    goalProgress.setAttribute("style", "width: " + GOAL_PROGRESS + "%;")
    goalProgressText.textContent = `${GOAL_PROGRESS}%`

    if (IS_GOAL_ANIMATED) {
        goalProgress.setAttribute("data-animated", "")
    }
    if (GOAL_AMOUNT) {
        goalAmount.textContent = GOAL_AMOUNT
        goalProgressText.textContent = `[${GOAL_PROGRESS}%]`
    }
} catch (e) {
    console.log("Goal Module is not enabled.")
}
{% endif %}