(() => {
  const form = document.getElementById("guided-workout-form");
  if (!form) return;

  const checks = [...form.querySelectorAll('input[name="completed_exercise[]"]')];
  const count = document.getElementById("completion-count");
  const updateCount = () => {
    const complete = checks.filter((check) => check.checked).length;
    count.textContent = `${complete} of ${checks.length} movements complete`;
  };
  checks.forEach((check) => check.addEventListener("change", () => {
    check.closest(".movement-card").classList.toggle("movement-completed", check.checked);
    updateCount();
  }));

  document.querySelectorAll(".exercise-demo-sequence").forEach((photo) => {
    const canvas = photo.closest(".movement-demo-canvas");
    const toggle = canvas.querySelector(".demo-toggle");
    const step = canvas.querySelector(".demo-step");
    const frameCount = canvas.querySelector(".demo-frame-count");
    const frames = [photo.getAttribute("src"), photo.dataset.nextFrame];
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const nextFrame = new Image();
    nextFrame.src = frames[1];
    let currentFrame = 0;
    let timer = null;

    const showFrame = (index) => {
      currentFrame = index;
      photo.src = frames[index];
      photo.dataset.currentFrame = String(index);
      photo.alt = `${photo.dataset.exerciseName} ${index === 0 ? "starting" : "finishing"} position`;
      frameCount.firstChild.textContent = `0${index + 1} `;
    };

    const pause = () => {
      if (timer !== null) window.clearInterval(timer);
      timer = null;
      toggle.setAttribute("aria-pressed", "true");
      toggle.setAttribute("aria-label", "Play movement demo");
      toggle.textContent = "▶";
    };

    const play = () => {
      if (timer !== null) return;
      toggle.setAttribute("aria-pressed", "false");
      toggle.setAttribute("aria-label", "Pause movement demo");
      toggle.textContent = "Ⅱ";
      timer = window.setInterval(() => showFrame(currentFrame === 0 ? 1 : 0), 2200);
    };

    step.addEventListener("click", () => showFrame(currentFrame === 0 ? 1 : 0));
    toggle.addEventListener("click", () => {
      if (timer === null) play();
      else pause();
    });
    if (reducedMotion) pause();
    else play();
  });

  let timer = null;
  let activeButton = null;
  document.querySelectorAll(".rest-button").forEach((button) => {
    button.addEventListener("click", () => {
      if (timer) window.clearInterval(timer);
      if (activeButton) {
        activeButton.disabled = false;
        activeButton.innerHTML = `⏱ <span>Rest ${activeButton.dataset.seconds}s</span>`;
      }
      let remaining = Number(button.dataset.seconds);
      if (!Number.isFinite(remaining) || remaining < 1) return;
      activeButton = button;
      button.disabled = true;
      button.innerHTML = `⏱ <span>${remaining}s left</span>`;
      timer = window.setInterval(() => {
        remaining -= 1;
        if (remaining <= 0) {
          window.clearInterval(timer);
          timer = null;
          button.disabled = false;
          button.innerHTML = "✓ <span>Rest complete</span>";
          activeButton = null;
          return;
        }
        button.querySelector("span").textContent = `${remaining}s left`;
      }, 1000);
    });
  });

  form.addEventListener("submit", (event) => {
    if (!checks.some((check) => check.checked)) {
      event.preventDefault();
      count.textContent = "Mark at least one movement complete to save.";
      checks[0]?.focus();
    }
  });
})();
