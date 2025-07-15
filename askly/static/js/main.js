 AOS.init();

    function toggleTheme() {
      const body = document.body;
      const icon = document.getElementById("theme-icon");
      body.classList.toggle("dark");
      const isDark = body.classList.contains("dark");
      icon.classList.toggle("fa-moon", !isDark);
      icon.classList.toggle("fa-sun", isDark);
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    window.addEventListener("DOMContentLoaded", () => {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'dark') {
        document.body.classList.add('dark');
        const icon = document.getElementById("theme-icon");
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
      }
    });