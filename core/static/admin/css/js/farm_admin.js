document.addEventListener("DOMContentLoaded", function () {
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion) return;

    // --- Gentle reveal for the main content area on page load ---
    var content = document.getElementById("content");
    if (content) {
        content.classList.add("farm-fade-in");
    }

    // --- Top progress bar while navigating to the next page ---
    var bar = document.createElement("div");
    bar.id = "farm-progress-bar";
    document.body.appendChild(bar);

    function startProgressBar() {
        bar.style.transition = "none";
        bar.style.width = "0%";
        bar.style.opacity = "1";
        // Force reflow so the transition below actually animates from 0%
        void bar.offsetWidth;
        bar.style.transition = "width 0.5s ease, opacity 0.2s ease";
        bar.style.width = "75%";
    }

    document.querySelectorAll("a[href]").forEach(function (link) {
        var href = link.getAttribute("href") || "";
        if (link.target === "_blank" || href.startsWith("#") || href.startsWith("javascript:")) {
            return;
        }
        link.addEventListener("click", startProgressBar);
    });

    document.querySelectorAll("form").forEach(function (form) {
        form.addEventListener("submit", startProgressBar);
    });
});
