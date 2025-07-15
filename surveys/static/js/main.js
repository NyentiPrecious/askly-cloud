document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body;

    // 1. Initialize theme from localStorage
    const savedTheme = localStorage.getItem("theme") || "light";
    body.classList.remove("light", "dark");
    body.classList.add(savedTheme);

    // Set correct icon
    if (savedTheme === "dark") {
        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");
    } else {
        themeIcon.classList.remove("fa-sun");
        themeIcon.classList.add("fa-moon");
    }

    // 2. Toggle theme
    themeToggle.addEventListener("click", () => {
        const isDark = body.classList.contains("dark");
        body.classList.toggle("dark", !isDark);
        body.classList.toggle("light", isDark);

        if (isDark) {
            themeIcon.classList.remove("fa-sun");
            themeIcon.classList.add("fa-moon");
            localStorage.setItem("theme", "light");
        } else {
            themeIcon.classList.remove("fa-moon");
            themeIcon.classList.add("fa-sun");
            localStorage.setItem("theme", "dark");
        }
    });

    // 3. Initialize charts after delay (to allow styles to settle)
    setTimeout(() => {
        const ctx1 = document.getElementById("completionRateChart")?.getContext("2d");
        if (ctx1) {
            new Chart(ctx1, {
                type: "line",
                data: {
                    labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
                    datasets: [{
                        label: "Completion Rate",
                        data: [75, 82, 90, 88],
                        backgroundColor: "rgba(124, 58, 237, 0.5)",
                        borderColor: "#7C3AED",
                        borderWidth: 2
                    }]
                }
            });
        }

        const ctx2 = document.getElementById("responseBreakdownChart")?.getContext("2d");
        if (ctx2) {
            new Chart(ctx2, {
                type: "pie",
                data: {
                    labels: ["Agree", "Neutral", "Disagree"],
                    datasets: [{
                        label: "Responses",
                        data: [60, 25, 15],
                        backgroundColor: ["#FACC15", "#10B981", "#EF4444"]
                    }]
                }
            });
        }
    }, 500);

    // 4. AOS Animation Init
    AOS.init();

    // 5. Mobile menu toggle
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    menuToggle?.addEventListener("click", () => {
        navLinks?.classList.toggle("active");
    });
});







function filterSurveys() {
  const searchInput = document.getElementById("surveySearch").value.toLowerCase();
  const filterValue = document.getElementById("surveyFilter").value;
  const surveys = document.querySelectorAll(".survey-card");

  surveys.forEach(survey => {
    const title = survey.querySelector("h3").innerText.toLowerCase();
    const status = survey.getAttribute("data-status");

    if ((title.includes(searchInput) || !searchInput) && (filterValue === "all" || status === filterValue)) {
      survey.style.display = "block";
    } else {
      survey.style.display = "none";
    }
  });
}

function updateTitle(surveyId, newTitle) {
  fetch(`/update-survey-title/${surveyId}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: newTitle })
  });
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
    .then(() => alert("Survey link copied!"))
    .catch(err => console.error("Copy failed:", err));
}

function toggleArchive(surveyId, btn) {
  fetch(`/surveys/archive/${surveyId}/`, { method: "POST" })
    .then(() => {
      btn.classList.toggle("archived");
      btn.querySelector("i").classList.toggle("fas");
      btn.querySelector("i").classList.toggle("far");
    });
}

function openPreview(surveyId) {
  const modal = document.getElementById("preview-modal");
  const body = document.getElementById("modal-body");

  modal.classList.remove("hidden");
  body.innerHTML = "<p>Loading preview...</p>";

  fetch(`/surveys/preview/${surveyId}/`)
    .then(res => res.text())
    .then(html => {
      body.innerHTML = html;
    });
}

function closePreview() {
  document.getElementById("preview-modal").classList.add("hidden");
}