/* One controller owns product dialogs and confirmed basket updates. No client price calculations. */
(function () {
    'use strict';
    const packageModal = document.querySelector('dialog[data-modal-type="package"]');
    const content = packageModal && packageModal.querySelector('.modal__content__box');
    const drawer = document.getElementById('tzCartDrawer');
    const backdrop = document.getElementById('tzCartOverlay');
    let previousFocus = null;
    let drawerFocus = null;
    let productRequest = null;
    let requestVersion = 0;
    let mutating = false;

    function localURL(value) {
        const url = new URL(value, window.location.href);
        if (url.origin !== window.location.origin) throw new Error('Enlace de tienda no válido.');
        return url;
    }
    function focusable(root) {
        return Array.from(root.querySelectorAll('a[href], button:not([disabled]), input:not([type="hidden"]):not([disabled]), select, textarea, [tabindex="0"]')).filter(el => !el.hidden && el.getClientRects().length);
    }
    function closeModal() {
        requestVersion++;
        if (productRequest) productRequest.abort();
        document.querySelectorAll('dialog[data-modal-type][open]').forEach(modal => modal.close());
        document.body.removeAttribute('data-modal-opened');
        if (previousFocus && previousFocus.isConnected) previousFocus.focus();
    }
    function openDrawer() {
        if (!drawer || !backdrop) { window.location.assign('/checkout/basket'); return; }
        closeModal();
        drawerFocus = document.activeElement;
        drawer.hidden = false; drawer.inert = false; backdrop.hidden = false;
        requestAnimationFrame(() => { drawer.classList.add('is-active'); backdrop.classList.add('is-active'); });
        document.body.style.overflow = 'hidden';
        const first = drawer.querySelector('#tzCartCloseBtn');
        if (first) first.focus();
    }
    function closeDrawer() {
        if (!drawer || !backdrop) return;
        drawer.classList.remove('is-active'); backdrop.classList.remove('is-active');
        drawer.inert = true; drawer.hidden = true; backdrop.hidden = true;
        document.body.style.overflow = '';
        if (drawerFocus && drawerFocus.isConnected) drawerFocus.focus();
    }
    function openLogin() {
        closeModal(); closeDrawer();
        if (typeof window.tzOpenLoginModal === 'function') window.tzOpenLoginModal();
        else window.location.assign('/login');
    }
    function report(text, root) {
        const scope = root || packageModal || drawer || document.body;
        let message = scope.querySelector('[data-tz-error]');
        if (!message) {
            message = document.createElement('div'); message.dataset.tzError = '';
            message.className = 'tz-theme-error'; message.setAttribute('role', 'alert');
            scope.appendChild(message);
        }
        message.replaceChildren();
        const paragraph = document.createElement('p'); paragraph.textContent = text;
        message.appendChild(paragraph);
        const link = document.createElement('a'); link.href = '/checkout/basket'; link.textContent = 'Revisar mi carrito';
        message.appendChild(link);
    }
    function quantity(root, id) {
        const state = root.querySelector('#tz-basket-state');
        if (!state) return 0;
        const row = Array.from(state.querySelectorAll('[data-basket-package]')).find(el => el.dataset.basketPackage === id);
        return row ? parseInt(row.dataset.quantity, 10) || 0 : 0;
    }
    function syncBasket(doc) {
        const state = doc.querySelector('#tz-basket-state');
        if (!state) throw new Error('No se recibió el estado confirmado del carrito.');
        const old = document.getElementById('tz-basket-state');
        if (old) old.replaceWith(document.importNode(state, true));
        if (drawer) {
            const incoming = doc.getElementById('tzCartDrawer');
            if (!incoming) throw new Error('No se pudo actualizar el resumen del carrito.');
            ['.tz-cart-drawer-body', '.tz-cart-drawer-footer'].forEach(selector => {
                const next = incoming.querySelector(selector), current = drawer.querySelector(selector);
                if (next && current) current.replaceWith(document.importNode(next, true));
            });
        }
        document.querySelectorAll('[data-tz-cart-total], #tzNavCartPriceVal, #tzDrawerTotalPrice').forEach(el => {
            el.textContent = state.dataset.totalDisplay;
        });
        const count = Array.from(state.querySelectorAll('[data-quantity]')).reduce((sum, el) => sum + (parseInt(el.dataset.quantity, 10) || 0), 0);
        if (window.tzUpdateCartCount) window.tzUpdateCartCount(count);
        // If an ident changed, a previously rendered payment component must be refreshed before paying.
        const payment = document.getElementById('tebex-checkout');
        if (payment && state.dataset.ident) payment.setAttribute('ident', state.dataset.ident);
    }
    async function openPackage(value, trigger) {
        const url = localURL(value);
        if (!packageModal || !content || typeof packageModal.showModal !== 'function') {
            window.location.assign(url.href); return;
        }
        if (productRequest) productRequest.abort();
        const version = ++requestVersion;
        productRequest = new AbortController();
        previousFocus = trigger || document.activeElement;
        content.replaceChildren();
        const loading = document.createElement('p'); loading.className = 'tz-theme-error'; loading.textContent = 'Cargando detalles del paquete…'; content.appendChild(loading);
        if (!packageModal.open) packageModal.showModal();
        document.body.setAttribute('data-modal-opened', '');
        try {
            const response = await fetch(url.href, { credentials: 'same-origin', cache: 'no-store', signal: productRequest.signal });
            if (!response.ok) throw new Error('No se pudo cargar el paquete. Puedes intentarlo de nuevo.');
            const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
            if (version !== requestVersion || !packageModal.open) return;
            const fragment = doc.querySelector('.package__modal');
            if (!fragment) throw new Error('Este paquete no está disponible.');
            const style = doc.querySelector('style[data-tz-package-style]');
            if (style && !document.getElementById('tz-package-style')) {
                const copy = document.importNode(style, true); copy.id = 'tz-package-style'; document.head.appendChild(copy);
            }
            content.replaceChildren(document.importNode(fragment, true));
            const title = content.querySelector('.tz-modal-pkg-name');
            if (title) { title.id = 'tz-active-package-title'; packageModal.setAttribute('aria-labelledby', title.id); }
            const close = content.querySelector('.modal__content--close');
            if (close) close.focus();
        } catch (error) {
            if (error.name === 'AbortError' || version !== requestVersion) return;
            content.replaceChildren();
            const close = document.createElement('button'); close.type = 'button'; close.className = 'modal__content--close'; close.textContent = 'Cerrar'; content.appendChild(close);
            report(error.message, content); close.focus();
        }
    }
    async function addToBasket(button) {
        const url = localURL(button.dataset.addUrl || button.href);
        if (button.hasAttribute('data-cart-modal-login')) { openLogin(); return; }
        const match = url.pathname.match(/^\/checkout\/packages\/add\/([^/]+)\/(single|subscribe)$/);
        if (!match || button.dataset.nativeOptions === 'true') { window.location.assign(url.href); return; }
        if (mutating) return;
        const id = decodeURIComponent(match[1]);
        const before = quantity(document, id);
        const scope = button.closest('.package__modal, .tz-card') || button.parentElement;
        const name = scope.querySelector('.tz-modal-pkg-name, .tz-card-title');
        const image = scope.querySelector('.tz-modal-img-wrap img, .tz-card-image-wrap img');
        mutating = true; button.setAttribute('aria-busy', 'true');
        if ('disabled' in button) button.disabled = true;
        try {
            const response = await fetch(url.href, { credentials: 'same-origin', cache: 'no-store' });
            if (!response.ok) throw new Error('Tebex no confirmó la operación. Revisa el carrito antes de reintentar.');
            const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
            const message = doc.querySelector('[data-tz-message]');
            if (response.headers.get('x-package-action-status')?.toLowerCase() === 'failed') throw new Error(message ? message.textContent.trim() : 'No se pudo añadir este paquete.');
            if (doc.querySelector('form.store-product-options, .store-product-options form, [data-popup].store-product-options')) {
                // This GET has only requested options; let Tebex render and validate the real form.
                window.location.assign(localURL(response.url).href); return;
            }
            const state = doc.querySelector('#tz-basket-state');
            if (!state) throw new Error('No se pudo confirmar el cambio. Revisa el carrito; no se ha repetido la petición.');
            const after = quantity(doc, id);
            if (!after) throw new Error(message ? message.textContent.trim() : 'El paquete no se añadió. Consulta sus opciones o requisitos.');
            syncBasket(doc);
            if (window.tzShowAddedPopup) window.tzShowAddedPopup(after > before ? (name ? name.textContent.trim() : 'Paquete') : 'El paquete ya está en tu carrito', image ? image.src : '', 'Total del carrito: ' + state.dataset.totalDisplay);
            openDrawer();
        } catch (error) {
            report(error.message, scope);
        } finally {
            mutating = false; button.removeAttribute('aria-busy');
            if ('disabled' in button) button.disabled = false;
        }
    }
    document.addEventListener('click', event => {
        if (!(event.target instanceof Element)) return;
        const target = event.target;
        const close = target.closest('.modal__content--close, .tz-close-modal-btn, .tz-close-btn');
        if (close) { event.preventDefault(); closeModal(); return; }
        if (target.closest('#tzOpenCartBtn')) { event.preventDefault(); openDrawer(); return; }
        if (target.closest('#tzCartCloseBtn') || target === backdrop) { event.preventDefault(); closeDrawer(); return; }
        if (target.closest('#tzCartRequireLoginBtn, [data-cart-modal-login]')) { event.preventDefault(); openLogin(); return; }
        const add = target.closest('.tz-btn-add-cart[data-add-url]');
        if (add) { event.preventDefault(); addToBasket(add).catch(error => report(error.message)); return; }
        const product = target.closest('.triplezone__toogle--modal[data-remote]');
        if (product) { event.preventDefault(); openPackage(product.dataset.remote, product).catch(error => report(error.message)); return; }
        const modalButton = target.closest('[data-modal-toggler]');
        if (modalButton) {
            const modal = Array.from(document.querySelectorAll('dialog[data-modal-type]')).find(el => el.dataset.modalType === modalButton.dataset.modalToggler);
            if (modal && typeof modal.showModal === 'function') { event.preventDefault(); previousFocus = modalButton; modal.showModal(); modal.removeAttribute('data-loading-modal'); }
        }
    });
    document.querySelectorAll('dialog[data-modal-type]').forEach(modal => {
        modal.addEventListener('click', event => { if (event.target === modal) closeModal(); });
        modal.addEventListener('cancel', event => { event.preventDefault(); closeModal(); });
    });
    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && drawer && !drawer.hidden) { event.preventDefault(); closeDrawer(); }
        if (event.key === 'Tab' && drawer && !drawer.hidden) {
            const controls = focusable(drawer); if (!controls.length) return;
            if (event.shiftKey && document.activeElement === controls[0]) { event.preventDefault(); controls[controls.length - 1].focus(); }
            else if (!event.shiftKey && document.activeElement === controls[controls.length - 1]) { event.preventDefault(); controls[0].focus(); }
        }
    });
    document.addEventListener('error', event => {
        const image = event.target;
        if (image instanceof HTMLImageElement && image.src.includes('minotar.net') && !image.dataset.fallbackUsed) {
            image.dataset.fallbackUsed = 'true'; image.src = 'https://minotar.net/avatar/MHF_Question/48';
        }
    }, true);
    window.closeModal = closeModal;
    window.tzCloseModal = closeModal;
    window.tzOpenCartDrawer = openDrawer;
    window.tzCloseCartDrawer = closeDrawer;
    window.tzSyncBasket = syncBasket;
})();
