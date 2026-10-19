/* iziModal remains available only for legacy, non-Minecraft authentication. */
if (window.jQuery && window.jQuery.fn.iziModal && document.getElementById('modal-login')) {
    window.jQuery('#modal-login').iziModal({ width: 600, overlayClose: true, closeOnEscape: true });
}
