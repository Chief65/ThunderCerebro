let cooldown;

jQuery(document).ready(function (e) {
    function t(t) {
        e(t).bind('click', function (t) {
            t.preventDefault();
            e(this).parent().fadeOut();
        });
    }

    e('.dropdown-toggle__second').click(function () {
        var t = e(this)
            .parents('.triplezone__second--toggle-dropdown')
            .children('.triplezone__second--dropdown')
            .is(':hidden');
        e(
            '.triplezone__second--toggle-dropdown .triplezone__second--dropdown'
        ).slideUp(100, 'linear');
        e(
            '.triplezone__second--toggle-dropdown .dropdown-toggle__second'
        ).removeClass('active-dropdown');
        e('.triplezone__second--toggle-dropdown')
            .children('.dropdown-toggle__second')
            .children('i')
            .removeClass('rotire-carret');
        if (t) {
            e(this)
                .parents('.triplezone__second--toggle-dropdown')
                .children('.triplezone__second--dropdown')
                .slideToggle(100, 'linear')
                .parents('.triplezone__second--toggle-dropdown')
                .children('dropdown-toggle__second')
                .addClass('active-dropdown');
            e(this)
                .parents('.triplezone__second--toggle-dropdown')
                .children('.triplezone__second--dropdown')
                .parents('.triplezone__second--toggle-dropdown')
                .children('.dropdown-toggle__second')
                .children('i')
                .addClass('rotire-carret');
        }
    });

    $('.sidebar-header').click(function () {
        if ($(window).width() < 960) {
            $('.sidebar-header').toggleClass('sidebar-round');
            $('#toggle-mobile-nav').toggleClass('mobile-enabled');
            $('.sidebar-header .mdi-close').toggleClass('close-mobile');
            $('.sidebar-header .mdi-menu').toggleClass('close-mobile');
        }
    });

    e(document).bind('click', function (t) {
        var n = e(t.target);
        if (!n.parents().hasClass('triplezone__second--toggle-dropdown')) {
            e(
                '.triplezone__second--toggle-dropdown .triplezone__second--dropdown'
            ).slideUp(100, 'linear');
            e('.triplezone__second--toggle-dropdown')
                .children('.dropdown-toggle__second')
                .children('i')
                .removeClass('rotire-carret');
        }
    });
    e(document).bind('click', function (t) {
        var n = e(t.target);
        if (!n.parents().hasClass('triplezone__second--toggle-dropdown')) {
            e(
                '.triplezone__second--toggle-dropdown .dropdown-toggle__second'
            ).removeClass('active-dropdown');
            e('.triplezone__second--toggle-dropdown')
                .children('.dropdown-toggle__second')
                .children('i')
                .removeClass('rotire-carret');
        }
    });
});

let productOpen = cooldown;

jQuery(document).ready(function (e) {
    function t(t) {
        e(t).bind('click', function (t) {
            t.preventDefault();
            e(this).parent().fadeOut();
        });
    }
    e('.dropdown-toggle').click(function () {
        var t = e(this)
            .parents('.triplezone-toggle-dropdown')
            .children('.triplezone-dropdown')
            .is(':hidden');
        e('.triplezone-toggle-dropdown .triplezone-dropdown').slideUp(
            100,
            'linear'
        );
        e('.triplezone-toggle-dropdown .dropdown-toggle').removeClass(
            'active-dropdown'
        );
        e('.triplezone-toggle-dropdown')
            .children('.dropdown-toggle')
            .children('i')
            .removeClass('rotire-carret');
        if (t) {
            e(this)
                .parents('.triplezone-toggle-dropdown')
                .children('.triplezone-dropdown')
                .slideToggle(100, 'linear')
                .parents('.triplezone-toggle-dropdown')
                .children('.dropdown-toggle')
                .addClass('active-dropdown');
            e(this)
                .parents('.triplezone-toggle-dropdown')
                .children('.triplezone-dropdown')
                .parents('.triplezone-toggle-dropdown')
                .children('.dropdown-toggle')
                .children('i')
                .addClass('rotire-carret');
        }
    });
    e(document).bind('click', function (t) {
        var n = e(t.target);
        if (!n.parents().hasClass('triplezone-toggle-dropdown')) {
            e('.triplezone-toggle-dropdown .triplezone-dropdown').slideUp(
                100,
                'linear'
            );
            e('.triplezone-toggle-dropdown')
                .children('.dropdown-toggle')
                .children('i')
                .removeClass('rotire-carret');
        }
    });
    e(document).bind('click', function (t) {
        var n = e(t.target);
        if (!n.parents().hasClass('triplezone-toggle-dropdown')) {
            e('.triplezone-toggle-dropdown .dropdown-toggle').removeClass(
                'active-dropdown'
            );
            e('.triplezone-toggle-dropdown')
                .children('.dropdown-toggle')
                .children('i')
                .removeClass('rotire-carret');
        }
    });
});