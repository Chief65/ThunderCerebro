// ===== SIDEBAR CARRITO NATIVO =====
(function() {

    function openCart() {
        $('#modal').addClass('tz-cart-open');
        $('#tz-cart-backdrop').addClass('tz-cart-open');
        $('body').css('overflow', 'hidden');
    }

    function closeCart() {
        $('#modal').removeClass('tz-cart-open');
        $('#tz-cart-backdrop').removeClass('tz-cart-open');
        $('body').css('overflow', '');
    }

    $(document).ready(function() {

        // Crear backdrop
        $('body').append('<div id="tz-cart-backdrop"></div>');

        // Añadir estilos del sidebar
        $('<style>')
            .text([
                '#modal {',
                '  display: block !important;',
                '  position: fixed !important;',
                '  top: 0 !important;',
                '  right: -420px !important;',
                '  left: auto !important;',
                '  width: 420px !important;',
                '  height: 100vh !important;',
                '  max-height: 100vh !important;',
                '  margin: 0 !important;',
                '  border-radius: 0 !important;',
                '  overflow-y: auto !important;',
                '  z-index: 9999 !important;',
                '  transition: right 0.3s cubic-bezier(.4,0,.2,1) !important;',
                '  background: var(--second-background) !important;',
                '}',
                '#modal.tz-cart-open {',
                '  right: 0 !important;',
                '}',
                '#tz-cart-backdrop {',
                '  display: block;',
                '  position: fixed;',
                '  inset: 0;',
                '  background: rgba(0,0,0,0.5);',
                '  z-index: 9998;',
                '  opacity: 0;',
                '  pointer-events: none;',
                '  transition: opacity 0.3s ease;',
                '}',
                '#tz-cart-backdrop.tz-cart-open {',
                '  opacity: 1;',
                '  pointer-events: all;',
                '}',
                '.shopping-cart-overlay { display: flex !important; flex-direction: column !important; min-height: 100vh !important; }',
                '.shopping-cart { display: flex !important; flex-direction: column !important; flex: 1 !important; min-height: 100vh !important; width: 100% !important; }',
                '.shopping-cart-body { flex: 1 !important; }',
            ].join('\n'))
            .appendTo('head');

        // Abrir carrito
        $(document).on('click', '.tz-navbar__profile', function(e) {
            e.preventDefault();
            e.stopPropagation();
            {% if basket.ign %}
                openCart();
            {% else %}
                $('#modal-login').iziModal('open');
            {% endif %}
        });

        // Cerrar con botón X
        $(document).on('click', '#close-cart-btn', function(e) {
            e.preventDefault();
            closeCart();
        });

        // Cerrar con backdrop
        $(document).on('click', '#tz-cart-backdrop', function() {
            closeCart();
        });

        // Cerrar con Escape
        $(document).on('keydown', function(e) {
            if (e.key === 'Escape') closeCart();
        });

    });

})();

// ===== MODAL LOGIN (se queda con iziModal) =====
if ($("#modal-login").length) {
    $("#modal-login").iziModal({
        title: '',
        subtitle: '',
        headerColor: '#88A0B9',
        background: "null",
        theme: '',
        icon: null,
        iconText: null,
        iconColor: '',
        rtl: false,
        width: 600,
        top: null,
        bottom: null,
        borderBottom: false,
        padding: 0,
        radius: 0,
        zindex: 999,
        iframe: false,
        iframeHeight: 400,
        iframeURL: null,
        focusInput: true,
        group: '',
        loop: false,
        arrowKeys: false,
        navigateCaption: false,
        navigateArrows: false,
        history: false,
        restoreDefaultContent: false,
        autoOpen: 0,
        bodyOverflow: false,
        fullscreen: false,
        openFullscreen: false,
        closeOnEscape: true,
        closeButton: true,
        appendTo: 'body',
        appendToOverlay: 'body',
        overlay: true,
        overlayClose: true,
        overlayColor: 'rgba(0, 0, 0, 0.4)',
        timeout: false,
        timeoutProgressbar: false,
        pauseOnHover: false,
        timeoutProgressbarColor: 'rgba(255,255,255,0.5)',
        transitionIn: 'comingIn',
        transitionOut: 'comingOut',
        transitionInOverlay: 'fadeIn',
        transitionOutOverlay: 'fadeOut',
        onFullscreen: function () { },
        onResize: function () { },
        onOpening: function () { },
        onOpened: function () { },
        onClosing: function () { },
        onClosed: function () { },
        afterRender: function () { }
    });
}