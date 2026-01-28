// static/app.js

/**
 * Simple client-side filtering:
 * - "Free only"
 * - By category
 */

function openEvent(url) {
    // Open event in a new tab
    window.open(url, "_blank", "noopener");
}

(function () {
    const buttons = document.querySelectorAll(".filter-btn");
    const cards = document.querySelectorAll(".event-card");

    function applyFilter(filter) {
        cards.forEach((card) => {
            const isFree = card.getAttribute("data-is-free") === "1";
            const category = card.getAttribute("data-category") || "Other";

            let visible = true;

            if (filter === "free") {
                visible = isFree;
            } else if (
                filter !== "all" &&
                filter !== "" &&
                ["Hackathon", "Workshop", "Meetup", "Conference", "Other"].includes(
                    filter
                )
            ) {
                visible = category === filter;
            }

            card.style.display = visible ? "block" : "none";
        });
    }

    buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const filter = btn.getAttribute("data-filter");
            applyFilter(filter);
        });
    });
})();
