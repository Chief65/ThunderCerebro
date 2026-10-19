(function () {
    const form = document.querySelector('#giftcardForm');
    if (!form) return;
    const back = document.querySelector('.giftcard__back--btn');
    const stage1 = document.querySelector('#giftcard__response--stage1');
    const stage2 = document.querySelector('#giftcard__response--stage2');
    if (back) back.addEventListener('click', () => { if (stage1) stage1.style.display = 'block'; if (stage2) stage2.style.display = 'none'; });
    let pending = false;
    form.addEventListener('submit', async event => {
        event.preventDefault();
        const input = document.querySelector('#giftcode');
        const cta = document.querySelector('[data-giftcard-state]');
        const status = document.querySelector('#status-giftcard');
        if (pending || !input || input.value.length < 4) return;
        pending = true;
        if (cta) cta.setAttribute('data-giftcard-state', 'loading');
        try {
            const response = await axios.post('/#giftcardbalance', new FormData(form));
            const doc = new DOMParser().parseFromString(response.data, 'text/html');
            const message = doc.querySelector('#rezultatGiftCard p');
            if (!message) throw new Error('No se pudo consultar el saldo. Inténtalo de nuevo.');
            if (status) status.textContent = message.textContent.trim();
            if (stage1) stage1.style.display = 'none';
            if (stage2) stage2.style.display = 'block';
        } catch (error) {
            if (status) { status.textContent = 'No se pudo consultar el saldo. Inténtalo de nuevo.'; status.setAttribute('role', 'alert'); }
        } finally {
            pending = false;
            if (cta) cta.setAttribute('data-giftcard-state', 'idle');
        }
    });
})();
