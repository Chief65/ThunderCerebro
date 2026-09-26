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

// Product Modal (Delegación global para elementos estáticos y dinámicos)
document.addEventListener("click", async (e) => {
    const button = e.target.closest(".triplezone__toogle--modal");
    if (!button) return;

    // Si el clic fue en el botón flotante quick-add, no abrir el modal de detalles
    if (e.target.closest(".tz-card-quick-add")) return;

    const removePackage = button.getAttribute("data-remote");
    if (!removePackage) return;

    e.preventDefault();

    try {
        if (!packageModal) return;

        // Limpiar inmediatamente el contenido previo y mostrar placeholder de carga suave
        if (modalContent) {
            modalContent.innerHTML = 
                '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:380px;gap:14px;color:#94a3b8;font-family:sans-serif;">' +
                    '<i class="mdi mdi-loading mdi-spin" style="font-size:36px;color:#facc15;"></i>' +
                    '<span style="font-size:13px;font-weight:700;letter-spacing:0.3px;">Cargando información...</span>' +
                '</div>';
        }

        packageModal.showModal();
        bodyElement.setAttribute('data-modal-opened', '');

        const response = await fetch(removePackage);
        const parser = new DOMParser();

        if (response.ok) {
            removeLoadingModal();

            const data = await response.text();
            const dataModalHTML = parser.parseFromString(data, "text/html");

            if (modalContent) {
                modalContent.style.opacity = '0';
                modalContent.style.transition = 'opacity 0.2s ease';
                modalContent.innerHTML = new XMLSerializer().serializeToString(dataModalHTML);
                requestAnimationFrame(() => {
                    modalContent.style.opacity = '1';
                });
            }
            
            {% include 'sliderAddon.js' ignore missing %}

            // Delegación de formularios de regalo o scripts específicos
            const giftButton = document.querySelector('[data-type-cta="gift"]');
            giftButton?.addEventListener("click", toggleGiftForm);
            
            // Close the modal if the user is not logged in
            document.querySelectorAll("[data-cart-modal-login]").forEach(loginBtn => {
                loginBtn.addEventListener("click", (evt) => {
                    evt.preventDefault();
                    closeModal();
                    $("#modal-login").iziModal("open");
                });
            });

        } else {
            closeModal();
        }

    } catch (error) {
        console.log(error);
        closeModal();
    }
});

// Función global unificada para recalcular el drawer
function updateDrawerTotals() {
    let total = 0;
    let currency = "USD";
    let totalItems = 0;

    const cards = document.querySelectorAll(".tz-cart-item-card");
    cards.forEach(card => {
        const qtyEl = card.querySelector(".tz-cart-qty-num") || card.querySelector(".tz-cart-item-meta span:first-child");
        const priceEl = card.querySelector(".tz-cart-item-price");

        if (qtyEl && priceEl) {
            const qtyMatch = qtyEl.textContent.match(/\d+/);
            const qty = qtyMatch ? parseInt(qtyMatch[0], 10) : 1;
            const priceText = priceEl.textContent;
            const numMatch = priceText.match(/[\d]+([.,][\d]{1,2})?/);
            const priceNum = numMatch ? parseFloat(numMatch[0].replace(',', '.')) : 0;

            total += (priceNum * qty);
            totalItems += qty;

            if (priceText.includes("€") || priceText.includes("EUR")) currency = "EUR";
            else if (priceText.includes("$") || priceText.includes("USD")) currency = "USD";
        }
    });

    const totalEl = document.getElementById("tzDrawerTotalPrice");
    if (totalEl) {
        totalEl.textContent = (currency === "EUR" ? total.toFixed(2) + " €" : "$" + total.toFixed(2));
    }

    const navPriceEl = document.getElementById("tzNavCartPriceVal");
    if (navPriceEl) {
        navPriceEl.textContent = (currency === "EUR" ? total.toFixed(2) + " €" : "$" + total.toFixed(2));
    }

    const summaryCount = document.querySelector(".tz-cart-summary-line span:last-child");
    if (summaryCount) {
        summaryCount.textContent = totalItems + " Items";
    }

    if (window.tzUpdateCartCount) {
        window.tzUpdateCartCount(totalItems);
    }

    const emptyState = document.getElementById("tzCartEmptyState");
    if (emptyState) {
        emptyState.style.display = totalItems === 0 ? "flex" : "none";
    }
}

// Delegación global para botones + y - de cantidad en el drawer (límite 99)
document.addEventListener("click", async (e) => {
    const plusBtn = e.target.closest(".tz-qty-plus");
    const minusBtn = e.target.closest(".tz-qty-minus");
    const removeBtn = e.target.closest(".tz-cart-item-remove");

    if (plusBtn) {
        e.preventDefault();
        const pkgId = plusBtn.getAttribute("data-pkg-id");
        const card = plusBtn.closest(".tz-cart-item-card");
        if (!card) return;

        const qtyNum = card.querySelector(".tz-cart-qty-num");
        const metaSpan = card.querySelector(".tz-cart-item-meta span:first-child");
        let count = parseInt(qtyNum.textContent, 10) || 1;

        if (count < 99) {
            count++;
            qtyNum.textContent = count;
            if (metaSpan) metaSpan.textContent = "Cant: " + count;

            fetch('/checkout/packages/add/' + pkgId + '/single').catch(() => {});
            updateDrawerTotals();
        }
    }

    if (minusBtn) {
        e.preventDefault();
        const pkgId = minusBtn.getAttribute("data-pkg-id");
        const card = minusBtn.closest(".tz-cart-item-card");
        if (!card) return;

        const qtyNum = card.querySelector(".tz-cart-qty-num");
        const metaSpan = card.querySelector(".tz-cart-item-meta span:first-child");
        let count = parseInt(qtyNum.textContent, 10) || 1;

        if (count > 1) {
            count--;
            qtyNum.textContent = count;
            if (metaSpan) metaSpan.textContent = "Cant: " + count;

            fetch('/checkout/packages/remove/' + pkgId).catch(() => {});
            updateDrawerTotals();
        } else {
            card.remove();
            fetch('/checkout/packages/remove/' + pkgId).catch(() => {});
            updateDrawerTotals();
        }
    }

    if (removeBtn) {
        e.preventDefault();
        const card = removeBtn.closest(".tz-cart-item-card");
        const removeHref = removeBtn.getAttribute("href");
        if (card) {
            card.remove();
            if (removeHref) fetch(removeHref).catch(() => {});
            updateDrawerTotals();
        }
    }
});

// Delegación global para el botón "Añadir al Carrito" de los modales de paquete
document.addEventListener("click", async (e) => {
    const addBtn = e.target.closest("#tzBtnAddToCartModal, .tz-btn-add-cart");
    if (!addBtn) return;

    if (addBtn.hasAttribute("data-cart-modal-login")) {
        e.preventDefault();
        closeModal();
        $("#modal-login").iziModal("open");
        return;
    }

    e.preventDefault();
    const targetUrl = addBtn.getAttribute("data-add-url") || addBtn.getAttribute("href");
    if (!targetUrl) return;

    const originalHtml = addBtn.innerHTML;
    addBtn.innerHTML = '<i class="mdi mdi-loading mdi-spin"></i> Agregando...';
    addBtn.style.pointerEvents = 'none';

    try {
        const response = await fetch(targetUrl);
        addBtn.innerHTML = originalHtml;
        addBtn.style.pointerEvents = 'all';

        // 1. Cerrar el modal del paquete
        closeModal();

        // 2. Extraer datos para el popup de confirmación
        const pkgNameEl = document.querySelector(".tz-modal-pkg-name") || document.querySelector(".tz-card-title");
        const pkgImgEl = document.querySelector(".tz-modal-img-wrap img") || document.querySelector(".tz-card img");
        const pkgPriceEl = document.querySelector(".tz-modal-price-val") || document.querySelector(".tz-card-price");

        const pkgTitle = pkgNameEl ? pkgNameEl.textContent.trim() : "Paquete";
        const pkgImg = pkgImgEl ? pkgImgEl.getAttribute("src") : "";
        const pkgPrice = pkgPriceEl ? pkgPriceEl.textContent.trim() : "";

        if (window.tzShowAddedPopup) {
            window.tzShowAddedPopup(pkgTitle, pkgImg, pkgPrice);
        }

        // 3. Incrementar el contador del carrito (+1 siempre)
        // Función para recalcular el Total a Pagar en tiempo real
        function recalculateDrawerTotal() {
            let total = 0;
            let currency = "USD";
            let totalItems = 0;

            document.querySelectorAll(".tz-cart-item-card").forEach(card => {
                const qtyEl = card.querySelector(".tz-cart-qty-num") || card.querySelector(".tz-cart-item-meta span:first-child");
                const priceEl = card.querySelector(".tz-cart-item-price");

                if (qtyEl && priceEl) {
                    const qtyMatch = qtyEl.textContent.match(/\d+/);
                    const qty = qtyMatch ? parseInt(qtyMatch[0], 10) : 1;
                    const priceText = priceEl.textContent;
                    const numMatch = priceText.match(/[\d]+([.,][\d]{1,2})?/);
                    const priceNum = numMatch ? parseFloat(numMatch[0].replace(',', '.')) : 0;

                    total += (priceNum * qty);
                    totalItems += qty;

                    if (priceText.includes("€") || priceText.includes("EUR")) currency = "EUR";
                    else if (priceText.includes("$") || priceText.includes("USD")) currency = "USD";
                }
            });

            const totalEl = document.getElementById("tzDrawerTotalPrice");
            if (totalEl) {
                totalEl.textContent = (currency === "EUR" ? total.toFixed(2) + " €" : "$" + total.toFixed(2));
            }

            const navPriceEl = document.getElementById("tzNavCartPriceVal");
            if (navPriceEl) {
                navPriceEl.textContent = (currency === "EUR" ? total.toFixed(2) + " €" : "$" + total.toFixed(2));
            }

            const summaryCount = document.querySelector(".tz-cart-summary-line span:last-child");
            if (summaryCount) {
                summaryCount.textContent = totalItems + " Items";
            }

            if (window.tzUpdateCartCount) {
                window.tzUpdateCartCount(totalItems);
            }
        }

        // 4. Actualizar visualmente la barra lateral (sidebar drawer) con Stackeo
        try {
            const emptyState = document.getElementById("tzCartEmptyState");
            if (emptyState) emptyState.style.display = "none";

            let itemsContainer = document.getElementById("tzCartItemsContainer");
            if (!itemsContainer) {
                const drawerBody = document.querySelector(".tz-cart-drawer-body");
                if (drawerBody) {
                    itemsContainer = document.createElement("div");
                    itemsContainer.className = "tz-cart-items-list";
                    itemsContainer.id = "tzCartItemsContainer";
                    drawerBody.appendChild(itemsContainer);
                }
            }

            if (itemsContainer) {
                // Verificar si el paquete ya existe en el drawer para stackear
                const pkgIdMatch = targetUrl.match(/\/add\/(\d+)/);
                const pkgId = pkgIdMatch ? pkgIdMatch[1] : "custom";
                const existingCard = itemsContainer.querySelector(`[data-cart-package-id='${pkgId}']`);

                if (existingCard) {
                    // Stackear: incrementar la cantidad existente (máximo 99)
                    const qtyNumEl = existingCard.querySelector(".tz-cart-qty-num");
                    const metaSpan = existingCard.querySelector(".tz-cart-item-meta span:first-child");
                    let currentQ = qtyNumEl ? parseInt(qtyNumEl.textContent, 10) : 1;
                    if (currentQ < 99) {
                        currentQ++;
                        if (qtyNumEl) qtyNumEl.textContent = currentQ;
                        if (metaSpan) metaSpan.textContent = "Cant: " + currentQ;
                    }
                } else {
                    // Crear nueva tarjeta con controles + y -
                    const itemCard = document.createElement("div");
                    itemCard.className = "tz-cart-item-card";
                    itemCard.setAttribute("data-cart-package-id", pkgId);
                    itemCard.innerHTML = 
                        '<div class="tz-cart-item-main">' +
                            (pkgImg ? '<img src="' + pkgImg + '" alt="' + pkgTitle + '" class="tz-cart-item-img">' : '<div class="tz-cart-item-img-placeholder"><i class="mdi mdi-cube-outline"></i></div>') +
                            '<div class="tz-cart-item-details">' +
                                '<span class="tz-cart-item-name">' + pkgTitle + '</span>' +
                                '<div class="tz-cart-item-meta">' +
                                    '<span>Cant: 1</span>' +
                                    '<span>•</span>' +
                                    '<span class="tz-cart-item-price">' + pkgPrice + '</span>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="tz-cart-item-actions">' +
                            '<div class="tz-cart-qty-pill">' +
                                '<button type="button" class="tz-cart-qty-btn tz-qty-minus" data-pkg-id="' + pkgId + '" aria-label="Disminuir">−</button>' +
                                '<span class="tz-cart-qty-num" id="tz-drawer-qty-' + pkgId + '">1</span>' +
                                '<button type="button" class="tz-cart-qty-btn tz-qty-plus" data-pkg-id="' + pkgId + '" aria-label="Aumentar">+</button>' +
                            '</div>' +
                            '<a href="' + targetUrl.replace('/add/', '/remove/') + '" class="tz-cart-item-remove" title="Eliminar del carrito">' +
                                '<i class="mdi mdi-trash-can-outline"></i>' +
                            '</a>' +
                        '</div>';
                    itemsContainer.appendChild(itemCard);
                }
            }

            recalculateDrawerTotal();
        } catch (e) {
            console.log(e);
        }

        // 5. Abrir la barra lateral del carrito
        setTimeout(() => {
            if (typeof window.tzOpenCartDrawer === "function") {
                window.tzOpenCartDrawer();
            } else {
                const openCartTrigger = document.getElementById("tzOpenCartBtn");
                if (openCartTrigger) openCartTrigger.click();
            }
        }, 150);

    } catch (err) {
        addBtn.innerHTML = originalHtml;
        addBtn.style.pointerEvents = 'all';
        window.location.href = targetUrl;
    }
});

// Delegación global para botones + y - de cantidad en el drawer (límite 99)
document.addEventListener("click", async (e) => {
    const plusBtn = e.target.closest(".tz-qty-plus");
    const minusBtn = e.target.closest(".tz-qty-minus");

    if (plusBtn) {
        e.preventDefault();
        const pkgId = plusBtn.getAttribute("data-pkg-id");
        const card = plusBtn.closest(".tz-cart-item-card");
        if (!card) return;

        const qtyNum = card.querySelector(".tz-cart-qty-num");
        const metaSpan = card.querySelector(".tz-cart-item-meta span:first-child");
        let count = parseInt(qtyNum.textContent, 10) || 1;

        if (count < 99) {
            count++;
            qtyNum.textContent = count;
            if (metaSpan) metaSpan.textContent = "Cant: " + count;

            // Sincronizar con el backend de Tebex
            fetch('/checkout/packages/add/' + pkgId + '/single').catch(() => {});
            
            // Recalcular total
            let total = 0;
            document.querySelectorAll(".tz-cart-item-card").forEach(c => {
                const q = parseInt(c.querySelector(".tz-cart-qty-num")?.textContent || "1", 10);
                const pMatch = c.querySelector(".tz-cart-item-price")?.textContent.match(/[\d]+([.,][\d]{1,2})?/);
                const p = pMatch ? parseFloat(pMatch[0].replace(',', '.')) : 0;
                total += (p * q);
            });
            const totalEl = document.getElementById("tzDrawerTotalPrice");
            if (totalEl) totalEl.textContent = "$" + total.toFixed(2);

            const badge = document.getElementById("tzCartBadgeCount");
            if (badge) {
                const curB = parseInt(badge.innerText, 10) || 0;
                badge.innerText = curB + 1;
            }
        }
    }

    if (minusBtn) {
        e.preventDefault();
        const pkgId = minusBtn.getAttribute("data-pkg-id");
        const card = minusBtn.closest(".tz-cart-item-card");
        if (!card) return;

        const qtyNum = card.querySelector(".tz-cart-qty-num");
        const metaSpan = card.querySelector(".tz-cart-item-meta span:first-child");
        let count = parseInt(qtyNum.textContent, 10) || 1;

        if (count > 1) {
            count--;
            qtyNum.textContent = count;
            if (metaSpan) metaSpan.textContent = "Cant: " + count;

            // Sincronizar disminución en el backend
            fetch('/checkout/packages/remove/' + pkgId).catch(() => {});

            // Recalcular total
            let total = 0;
            document.querySelectorAll(".tz-cart-item-card").forEach(c => {
                const q = parseInt(c.querySelector(".tz-cart-qty-num")?.textContent || "1", 10);
                const pMatch = c.querySelector(".tz-cart-item-price")?.textContent.match(/[\d]+([.,][\d]{1,2})?/);
                const p = pMatch ? parseFloat(pMatch[0].replace(',', '.')) : 0;
                total += (p * q);
            });
            const totalEl = document.getElementById("tzDrawerTotalPrice");
            if (totalEl) totalEl.textContent = "$" + total.toFixed(2);

            const badge = document.getElementById("tzCartBadgeCount");
            if (badge) {
                const curB = parseInt(badge.innerText, 10) || 1;
                badge.innerText = Math.max(0, curB - 1);
            }
        } else {
            // Si llega a 0, eliminar tarjeta
            card.remove();
            fetch('/checkout/packages/remove/' + pkgId).catch(() => {});
            
            const remaining = document.querySelectorAll(".tz-cart-item-card");
            if (remaining.length === 0) {
                const emptyState = document.getElementById("tzCartEmptyState");
                if (emptyState) emptyState.style.display = "flex";
                const totalEl = document.getElementById("tzDrawerTotalPrice");
                if (totalEl) totalEl.textContent = "$0.00";
                if (window.tzUpdateCartCount) window.tzUpdateCartCount(0);
            }
        }
    }
});

// Delegación para cerrar modal con el botón X
document.addEventListener("click", (e) => {
    if (e.target.closest(".tz-close-btn") || e.target.closest(".tz-close-modal-btn") || e.target.closest(".modal__content--close")) {
        e.preventDefault();
        closeModal();
    }
});

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
    const allModals = document.querySelectorAll("dialog.modal, dialog[data-modal-type], dialog");
    allModals.forEach(modal => {
        try {
            if (modal.open || modal.hasAttribute("open")) {
                modal.removeAttribute("closing");
                modal.close();
            }
        } catch (e) {
            modal.style.display = "none";
        }
    });

    document.querySelectorAll("body").forEach(b => {
        b.removeAttribute("data-modal-opened");
    });

    document.querySelectorAll(".modal[data-loading-modal]").forEach(m => {
        m.removeAttribute("data-loading-modal");
    });
}

window.closeModal = closeModal;
window.tzCloseModal = closeModal;

function onClickOutside(event) {
    modals.forEach(modal => {
        if (event.target === modal) {
            closeModal();
        }
    });
}