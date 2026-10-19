/* Native POST updates all basket quantities once. Tebex renders the authoritative total. */
(function () {
    document.addEventListener('click', function(event) {
        const button = event.target.closest('.tz-checkout-qty-btn');
        if (!button) return;
        const form = button.closest('form[data-tz-quantity-form]');
        if (!form) return;
        event.preventDefault();
        if (form.dataset.submitting) return;
        const input = Array.from(form.elements).find(el => el.name === button.dataset.package);
        if (!input || input.disabled || input.type === 'hidden') return;
        const current = parseInt(input.value, 10) || 1;
        const next = button.dataset.action === 'add' ? current + 1 : Math.max(1, current - 1);
        if (current === next) return;
        input.value = String(next);
        form.dataset.submitting = 'true'; form.setAttribute('aria-busy', 'true');
        // Native full response refreshes price, quantity and payment ident together.
        HTMLFormElement.prototype.submit.call(form);
    });
    const button = document.getElementById('purchase-button');
    const boxes = [document.getElementById('tzTermsCheckbox1'), document.getElementById('tzTermsCheckbox2')].filter(Boolean);
    const error = document.getElementById('tzTermsError');
    function validate() {
        const valid = boxes.length === 2 && boxes.every(box => box.checked);
        if (button) button.disabled = !valid;
        if (error) error.hidden = valid;
        return valid;
    }
    boxes.forEach(box => box.addEventListener('change', validate));
    if (button) button.addEventListener('click', event => {
        if (!validate()) { event.preventDefault(); event.stopImmediatePropagation(); }
    }, true);
    validate();
})();
