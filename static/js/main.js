document.addEventListener(
    "DOMContentLoaded",
    function () {

        /*
        ========================================
        THEME TOGGLE
        ========================================
        */

        const themeToggle = document.getElementById("themeToggle");
        const savedTheme = localStorage.getItem("nextgenai-theme");
        const systemTheme = window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
        const activeTheme = savedTheme || systemTheme;

        function applyTheme(theme) {
            document.documentElement.dataset.theme = theme;
            document.body.classList.toggle("light-mode", theme === "light");
            if (themeToggle) {
                const icon = themeToggle.querySelector("i");
                if (icon) icon.className = theme === "light" ? "bi bi-sun" : "bi bi-moon-stars";
                themeToggle.setAttribute("aria-label", `Switch to ${theme === "light" ? "dark" : "light"} theme`);
                themeToggle.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
            }
        }

        applyTheme(activeTheme);
        if (themeToggle) {
            themeToggle.addEventListener("click", function () {
                const nextTheme = document.documentElement.dataset.theme === "light" ? "dark" : "light";
                localStorage.setItem("nextgenai-theme", nextTheme);
                applyTheme(nextTheme);
            });
        }

        const searchToggle = document.getElementById("searchToggle");
        const searchPanel = document.getElementById("searchPanel");
        const searchClose = document.getElementById("searchClose");
        const searchInput = document.getElementById("searchInput");
        const searchForm = document.getElementById("searchForm");
        const searchResults = document.getElementById("searchResults");

        function closeSearch() {
            if (!searchPanel) return;
            searchPanel.hidden = true;
            if (searchToggle) searchToggle.setAttribute("aria-expanded", "false");
        }

        function renderSearchResults(results, query) {
            if (!searchResults) return;
            const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"
            }[character]));
            if (!results.length) {
                searchResults.innerHTML = `<p class="search-empty">No results found for “${escapeHtml(query)}”.</p>`;
                return;
            }
            searchResults.innerHTML = results.map((result) => `<article class="search-result"><span>${escapeHtml(result.category)}</span><h3>${escapeHtml(result.title)}</h3><p>${escapeHtml(result.description)}</p></article>`).join("");
        }

        if (searchToggle && searchPanel && searchInput) {
            searchToggle.addEventListener("click", function () {
                searchPanel.hidden = false;
                searchToggle.setAttribute("aria-expanded", "true");
                searchInput.focus();
            });
            searchClose?.addEventListener("click", closeSearch);
            searchForm?.addEventListener("submit", async function (event) {
                event.preventDefault();
                const query = searchInput.value.trim();
                if (!query) return;
                searchResults.innerHTML = '<p class="search-empty">Searching...</p>';
                try {
                    const response = await fetch(`/search/?q=${encodeURIComponent(query)}`, { headers: { "Accept": "application/json" } });
                    const data = await response.json();
                    renderSearchResults(data.results || [], query);
                } catch (error) {
                    searchResults.innerHTML = '<p class="search-empty">Search is temporarily unavailable.</p>';
                }
            });
            searchPanel.addEventListener("click", (event) => { if (event.target === searchPanel) closeSearch(); });
            document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeSearch(); });
        }

        const navbarCollapse = document.getElementById("mainNavbar");
        document.querySelectorAll("#mainNavbar .nav-link, #mainNavbar .navbar-actions a").forEach((link) => {
            link.addEventListener("click", () => {
                if (navbarCollapse && navbarCollapse.classList.contains("show")) {
                    bootstrap.Collapse.getOrCreateInstance(navbarCollapse).hide();
                }
            });
        });

        const path = window.location.pathname;
        document.querySelectorAll("[data-nav-key]").forEach((link) => {
            const key = link.dataset.navKey;
            const isActive = (key === "home" && path === "/") || (key === "about" && path === "/" && window.location.hash === "#about") || (key === "contact" && path === "/" && window.location.hash === "#contact") || (key === "team" && path.startsWith("/team/")) || (key === "events" && path.startsWith("/events/")) || (key === "projects" && path.startsWith("/projects/")) || (key === "achievements" && path.startsWith("/achievements/")) || (key === "resources" && path.startsWith("/resources/")) || (key === "dashboard" && path.startsWith("/management/"));
            link.classList.toggle("active", isActive);
        });



        /*
        ========================================
        ANIMATED COUNTERS
        ========================================
        */

        const counters =
            document.querySelectorAll(
                ".counter"
            );


        const animateCounter =
            function (counter) {

                const target =
                    Number(
                        counter.dataset.target
                    );


                let current = 0;


                const increment =
                    Math.max(
                        1,
                        Math.ceil(target / 40)
                    );


                const updateCounter =
                    function () {

                        current += increment;


                        if (current >= target) {

                            counter.textContent =
                                target;

                            return;

                        }


                        counter.textContent =
                            current;


                        requestAnimationFrame(
                            updateCounter
                        );

                    };


                updateCounter();

            };



        /*
        ========================================
        INTERSECTION OBSERVER
        ========================================
        */

        if ("IntersectionObserver" in window) {

            const counterObserver =
                new IntersectionObserver(
                    function (entries, observer) {

                        entries.forEach(
                            function (entry) {

                                if (
                                    entry.isIntersecting
                                ) {

                                    animateCounter(
                                        entry.target
                                    );

                                    observer.unobserve(
                                        entry.target
                                    );

                                }

                            }
                        );

                    },
                    {
                        threshold: 0.5
                    }
                );


            counters.forEach(
                function (counter) {

                    counterObserver.observe(
                        counter
                    );

                }
            );

        } else {

            counters.forEach(
                animateCounter
            );

        }



        /*
        ========================================
        SCROLL REVEAL
        ========================================
        */

        const revealElements =
            document.querySelectorAll(
                ".feature-card, .project-card, .vision-card"
            );


        revealElements.forEach(
            function (element) {

                element.style.opacity = "0";

                element.style.transform =
                    "translateY(25px)";

                element.style.transition =
                    "opacity 0.7s ease, transform 0.7s ease";

            }
        );


        if ("IntersectionObserver" in window) {

            const revealObserver =
                new IntersectionObserver(
                    function (entries, observer) {

                        entries.forEach(
                            function (entry) {

                                if (
                                    entry.isIntersecting
                                ) {

                                    entry.target.style.opacity =
                                        "1";

                                    entry.target.style.transform =
                                        "translateY(0)";

                                    observer.unobserve(
                                        entry.target
                                    );

                                }

                            }
                        );

                    },
                    {
                        threshold: 0.15
                    }
                );


            revealElements.forEach(
                function (element) {

                    revealObserver.observe(
                        element
                    );

                }
            );

        }



        /*
        ========================================
        NAVBAR SCROLL EFFECT
        ========================================
        */

        const navbar =
            document.querySelector(
                ".nextgen-navbar"
            );


        window.addEventListener(
            "scroll",
            function () {

                if (!navbar) {
                    return;
                }


                if (window.scrollY > 50) {

                    navbar.style.padding =
                        "10px 0";

                } else {

                    navbar.style.padding =
                        "18px 0";

                }

            }
        );



        /*
        ========================================
        SMOOTH NAVIGATION
        ========================================
        */

        document.querySelectorAll(
            'a[href^="#"]'
        ).forEach(
            function (link) {

                link.addEventListener(
                    "click",
                    function (event) {

                        const targetId =
                            this.getAttribute(
                                "href"
                            );


                        if (
                            targetId === "#" ||
                            !targetId
                        ) {

                            return;

                        }


                        const target =
                            document.querySelector(
                                targetId
                            );


                        if (target) {

                            event.preventDefault();


                            target.scrollIntoView(
                                {
                                    behavior: "smooth"
                                }
                            );

                        }

                    }
                );

            }
        );

    }
);