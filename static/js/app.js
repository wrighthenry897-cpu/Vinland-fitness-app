(() => {
  const menuToggle = document.getElementById("menu-toggle");
  const sidebar = document.getElementById("sidebar");
  if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", () => {
      const isOpen = sidebar.classList.toggle("mobile-open");
      menuToggle.setAttribute("aria-expanded", String(isOpen));
      menuToggle.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
      menuToggle.textContent = isOpen ? "×" : "☰";
    });
    document.addEventListener("click", (event) => {
      if (window.innerWidth <= 600 && sidebar.classList.contains("mobile-open")
          && !sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
        sidebar.classList.remove("mobile-open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "Open navigation");
        menuToggle.textContent = "☰";
      }
    });
  }

  document.querySelectorAll(".password-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const input = button.parentElement.querySelector("input");
      const showing = input.type === "password";
      input.type = showing ? "text" : "password";
      button.textContent = showing ? "HIDE" : "SHOW";
      button.setAttribute("aria-label", showing ? "Hide password" : "Show password");
    });
  });

  document.querySelectorAll(".flash-close").forEach((button) => {
    button.addEventListener("click", () => button.closest(".flash").remove());
  });

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });

  const rows = document.getElementById("exercise-rows");
  const template = document.getElementById("exercise-template");
  const addExercise = document.getElementById("add-exercise");
  if (rows && template && addExercise) {
    addExercise.addEventListener("click", () => {
      const fragment = template.content.cloneNode(true);
      const row = fragment.querySelector(".exercise-entry");
      row.querySelectorAll("input").forEach((input, index) => {
        const id = `exercise-new-${Date.now()}-${index}`;
        input.id = id;
        input.previousElementSibling.htmlFor = id;
      });
      rows.append(fragment);
      rows.lastElementChild.querySelector("input").focus();
    });
    rows.addEventListener("click", (event) => {
      const remove = event.target.closest(".remove-exercise");
      if (remove) remove.closest(".exercise-entry").remove();
    });
  }
})();
