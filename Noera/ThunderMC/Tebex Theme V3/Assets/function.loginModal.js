/* OAuth/Steam login links submit natively. Minecraft login is owned by tzLoginForm. */
document.querySelectorAll('[data-login-category]').forEach(function (link) {
    link.addEventListener('click', function (event) {
        event.preventDefault();
        if (window.tzCloseModal) window.tzCloseModal();
        if (window.tzOpenLoginModal) window.tzOpenLoginModal();
        else if (window.jQuery && window.jQuery.fn.iziModal && document.getElementById('modal-login')) window.jQuery('#modal-login').iziModal('open');
        else window.location.assign('/login');
    });
});
