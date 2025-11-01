// In base.html, after including cookie_banner.html
function loadAnalytics() {
    // Example: Google Analytics gtag
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID";
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', 'GA_MEASUREMENT_ID', { anonymize_ip: true });
}

function loadMarketing() {
    // Example placeholder for marketing pixel. Only load if consent.marketing === true.
}

// If consent cookie already exists, fire immediately; else banner will dispatch after user choice
window.addEventListener("cookie-consent-ready", function(e) {
    var consent = e.detail || {};
    if (consent.analytics) loadAnalytics();
    if (consent.marketing) loadMarketing();
});