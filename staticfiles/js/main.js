document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body;

    // Load saved theme preference
    const savedTheme = localStorage.getItem("theme") || "light";
    body.classList.add(savedTheme);
    themeIcon.classList.replace(savedTheme === "dark" ? "fa-moon" : "fa-sun", savedTheme === "dark" ? "fa-sun" : "fa-moon");

    themeToggle.addEventListener("click", () => {
        body.classList.toggle("dark");
        body.classList.toggle("light");

        const newTheme = body.classList.contains("dark") ? "dark" : "light";
        themeIcon.classList.replace(newTheme === "dark" ? "fa-moon" : "fa-sun", newTheme === "dark" ? "fa-sun" : "fa-moon");

        localStorage.setItem("theme", newTheme);
    });
});

























// function toggleTheme() {
//     const body = document.body;
//     const icon = document.getElementById("theme-icon");
//     body.classList.toggle("dark");
//     icon.classList.toggle("fa-moon");
//     icon.classList.toggle("fa-sun");
// }

// function toggleMenu() {
//     const navLinks = document.querySelector(".nav-links");
//     navLinks.classList.toggle("active");
// }

// window.addEventListener("scroll", function () {
//     const navbar = document.getElementById("navbar");
//     navbar.classList.toggle("scrolled", window.scrollY > 50);
// });

// document.addEventListener('DOMContentLoaded', function () {
//     AOS.init();
// });








//   document.addEventListener("DOMContentLoaded", () => {
//     const sections = document.querySelectorAll(".dashboard-section");
//     sections.forEach(section => {
//         section.classList.add("visible");
//     });
// });


    // document.addEventListener("DOMContentLoaded", () => {
    // const ctx = document.getElementById("surveyChart").getContext("2d");
    // new Chart(ctx, {
    //     type: "bar",
    //     data: {
    //         labels: ["Survey 1", "Survey 2", "Survey 3"],
    //         datasets: [{
    //             label: "Responses",
    //             data: [45, 78, 32],
    //             backgroundColor: ["#7c3aed", "#c084fc", "#5b21b6"]
    //         }]
    //     },
       