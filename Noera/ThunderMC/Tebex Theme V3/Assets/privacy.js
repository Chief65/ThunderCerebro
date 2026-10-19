/* Only the optional Analytics configured by this theme is controlled here. */
(function () {
    const banner = document.getElementById('tzAnalyticsConsent');
    if (!banner) return;
    const key = 'thundermc-analytics-consent-v1';
    let loaded = false;
    function read() { try { return localStorage.getItem(key); } catch (error) { return null; } }
    function allow() {
        if (loaded) return;
        const id = banner.dataset.analyticsId;
        if (!/^G-[A-Z0-9]+$|^UA-\d+-\d+$/i.test(id)) return;
        loaded = true;
        window['ga-disable-' + id] = false;
        window.dataLayer = window.dataLayer || [];
        window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
        window.gtag('consent', 'default', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
        window.gtag('js', new Date()); window.gtag('config', id);
        const script = document.createElement('script'); script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
        document.head.appendChild(script);
    }
    banner.querySelectorAll('[data-consent]').forEach(button => button.addEventListener('click', () => {
        const choice = button.dataset.consent;
        try { localStorage.setItem(key, choice); } catch (error) { /* Continue with this-page choice only. */ }
        banner.hidden = true;
        if (choice === 'yes') allow();
        else {
            window['ga-disable-' + banner.dataset.analyticsId] = true;
            if (window.gtag) window.gtag('consent', 'update', { analytics_storage: 'denied' });
        }
    }));
    document.querySelectorAll('[data-privacy-settings]').forEach(button => button.addEventListener('click', () => {
        banner.hidden = false; const first = banner.querySelector('button'); if (first) first.focus();
    }));
    if (read() === 'yes') allow();
    else if (read() !== 'no') banner.hidden = false;
})();
