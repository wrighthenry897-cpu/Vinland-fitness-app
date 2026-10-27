(() => {
  const FRAME_COUNT = 5;
  const FRAME_INTERVAL = 700;

  const nextFrame = (index, direction) => {
    let nextIndex = index + direction;
    if (nextIndex >= FRAME_COUNT) {
      nextIndex = FRAME_COUNT - 2;
      direction = -1;
    } else if (nextIndex < 0) {
      nextIndex = 1;
      direction = 1;
    }
    return { index: nextIndex, direction };
  };

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
    const transitionPhoto = photo.cloneNode(false);
    transitionPhoto.classList.add("exercise-demo-transition");
    transitionPhoto.src = frames[1];
    transitionPhoto.alt = "";
    transitionPhoto.setAttribute("aria-hidden", "true");
    canvas.append(transitionPhoto);
    frames.forEach((source) => {
      const image = new Image();
      image.src = source;
    });
    let currentFrame = 0;
    let frameDirection = 1;
    let timer = null;

    const showFrame = (index) => {
      currentFrame = index;
      frameCount.firstChild.textContent = `${String(index + 1).padStart(2, "0")} `;
      if (index === 0) {
        photo.alt = `${photo.dataset.exerciseName} ${photo.dataset.firstPosition} position`;
      } else if (index === FRAME_COUNT - 1) {
        photo.alt = `${photo.dataset.exerciseName} ${photo.dataset.secondPosition} position`;
      } else {
        photo.alt = `${photo.dataset.exerciseName} transitioning from ${photo.dataset.firstPosition} to ${photo.dataset.secondPosition}`;
      }
      transitionPhoto.style.opacity = String(index / (FRAME_COUNT - 1));
    };

    const advanceFrame = () => {
      const next = nextFrame(currentFrame, frameDirection);
      frameDirection = next.direction;
      showFrame(next.index);
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
      timer = window.setInterval(advanceFrame, FRAME_INTERVAL);
    };

    step.addEventListener("click", advanceFrame);
    toggle.addEventListener("click", () => {
      if (timer === null) play();
      else pause();
    });
    if (reducedMotion) pause();
    else play();
  });

  const player = document.getElementById("guided-player");
  const cards = [...form.querySelectorAll(".movement-card")];
  const startButton = document.getElementById("workout-start");
  if (player && cards.length && startButton) {
    const phaseLabel = document.getElementById("player-phase");
    const progressLabel = document.getElementById("player-progress");
    const progressSteps = document.getElementById("player-steps");
    const exerciseName = document.getElementById("player-exercise-name");
    const exerciseCue = document.getElementById("player-exercise-cue");
    const equipmentLabel = document.getElementById("player-equipment");
    const clock = document.getElementById("player-clock");
    const clockText = document.getElementById("player-clock-text");
    const clockCaption = document.getElementById("player-clock-caption");
    const timerRing = document.getElementById("player-timer-ring");
    const status = document.getElementById("player-status");
    const demoImage = document.getElementById("player-demo-image");
    const nextDemoImage = document.getElementById("player-demo-next");
    const setLabel = document.getElementById("player-set");
    const exercisePanel = document.getElementById("player-exercise");
    const upNextLabel = document.getElementById("player-up-next");
    const pauseButton = document.getElementById("workout-pause");
    const skipButton = document.getElementById("workout-skip");
    const voiceButton = document.getElementById("voice-toggle");
    const endButton = document.getElementById("workout-end");
    const saveButton = document.getElementById("workout-save");
    const supportsVoice = "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
    const circumference = 2 * Math.PI * 78;
    let exerciseIndex = 0;
    let setIndex = 0;
    let remaining = 0;
    let phase = "ready";
    let timer = null;
    let voiceEnabled = supportsVoice;
    let paused = false;
    let frameTimer = null;
    let blendFrame = 0;
    let blendDirection = 1;
    let restMovesForward = false;
    let introSequence = 0;

    const speak = (message) => {
      if (!voiceEnabled) return;
      window.speechSynthesis.cancel();
      const instruction = new SpeechSynthesisUtterance(message);
      instruction.rate = 0.9;
      instruction.pitch = 1;
      window.speechSynthesis.speak(instruction);
    };

    const exerciseIntroduction = (card) => {
      const name = card.dataset.exerciseName.toLowerCase();
      if (name.includes("plank") || name.includes("dead bug") || name.includes("bird dog") || name.includes("crunch")) {
        return "This one is all about core control. Moving slowly helps you stay steady and keep your breathing comfortable.";
      }
      if (name.includes("squat") || name.includes("lunge") || name.includes("calf raise") || name.includes("hinge") || name.includes("good morning")) {
        return "This is a lower-body strength move. Take your time finding a stable stance, and make each repetition smooth.";
      }
      if (name.includes("row") || name.includes("pulldown") || name.includes("pull-down") || name.includes("snow angel") || name.includes("cobra") || name.includes("superman")) {
        return "This movement works your back and posture muscles. Keep the motion controlled and let your shoulders stay relaxed.";
      }
      if (name.includes("curl") || name.includes("triceps") || name.includes("shoulder") || name.includes("push-up") || name.includes("pushup") || name.includes("press")) {
        return "This upper-body movement builds strength through a steady, controlled range. No need to rush; a comfortable pace is a strong start.";
      }
      return "This movement is a chance to build strength and control. Settle into a comfortable position and take it one step at a time.";
    };

    const speakExercise = (card, onComplete = () => {}) => {
      const sequence = ++introSequence;
      if (!voiceEnabled) {
        onComplete();
        return;
      }
      window.speechSynthesis.cancel();
      const intro = new SpeechSynthesisUtterance(
        `Before we begin, here's a little about ${card.dataset.exerciseName}. ${exerciseIntroduction(card)}`
      );
      const cue = new SpeechSynthesisUtterance(card.dataset.exerciseCue);
      intro.rate = 0.9;
      cue.rate = 0.9;
      intro.pitch = 1;
      cue.pitch = 1;
      let completed = false;
      const finishIntroduction = () => {
        if (completed || sequence !== introSequence) return;
        completed = true;
        onComplete();
      };
      cue.onend = finishIntroduction;
      cue.onerror = finishIntroduction;
      window.speechSynthesis.speak(intro);
      window.speechSynthesis.speak(cue);
    };

    const formatTime = (seconds) => `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
    const currentCard = () => cards[exerciseIndex];
    const updateClock = () => {
      clockText.textContent = formatTime(remaining);
      const total = Number(currentCard().dataset[phase === "work" ? "duration" : "rest"]);
      const progress = Math.max(0, Math.min(1, 1 - remaining / total));
      timerRing.style.strokeDashoffset = String(circumference * (1 - progress));
      clockCaption.textContent = phase === "rest" ? "REST" : "LEFT";
      phaseLabel.textContent = phase === "work" ? "YOUR MOVE" : "CATCH YOUR BREATH";
      player.classList.toggle("is-resting", phase === "rest");
      clock.setAttribute("aria-label", `${phase === "rest" ? "Rest" : "Exercise"}: ${formatTime(remaining)} remaining`);
      progressLabel.textContent = `MOVE ${String(exerciseIndex + 1).padStart(2, "0")} / ${String(cards.length).padStart(2, "0")}`;
      [...progressSteps.children].forEach((step, index) => {
        step.classList.toggle("is-current", index === exerciseIndex);
        step.classList.toggle("is-complete", checks[index].checked);
      });
    };

    checks.forEach((check) => check.addEventListener("change", updateClock));
    cards.forEach((_card, index) => {
      const step = document.createElement("span");
      step.setAttribute("aria-label", `Movement ${index + 1}`);
      progressSteps.append(step);
    });

    const stopFrames = () => {
      if (frameTimer !== null) window.clearInterval(frameTimer);
      frameTimer = null;
    };

    const animateMovement = (card) => {
      stopFrames();
      const startFrame = card.dataset.demoStart;
      const endFrame = card.dataset.demoEnd || startFrame;
      demoImage.classList.add("is-current");
      demoImage.src = startFrame;
      demoImage.alt = `${card.dataset.exerciseName} demonstration`;
      nextDemoImage.classList.add("is-current");
      nextDemoImage.src = endFrame;
      blendFrame = 0;
      blendDirection = 1;
      nextDemoImage.style.opacity = "0";
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (startFrame === endFrame || reducedMotion) return;
      frameTimer = window.setInterval(() => {
        const next = nextFrame(blendFrame, blendDirection);
        blendFrame = next.index;
        blendDirection = next.direction;
        nextDemoImage.style.opacity = String(blendFrame / (FRAME_COUNT - 1));
      }, FRAME_INTERVAL);
    };

    const loadExercise = (index, set = 0, announce = true) => {
      exerciseIndex = index;
      setIndex = set;
      const card = currentCard();
      const name = card.dataset.exerciseName;
      exerciseName.textContent = name;
      exerciseCue.textContent = card.dataset.exerciseCue;
      equipmentLabel.textContent = "NO EQUIPMENT";
      setLabel.textContent = `SET ${setIndex + 1} / ${Number(card.dataset.sets)} · ${card.querySelector(".movement-target").textContent}`;
      animateMovement(card);
      phase = "work";
      remaining = Number(card.dataset.duration);
      clockCaption.textContent = "LEFT";
      status.textContent = "Move at a comfortable pace. Modify the movement if you need to.";
      pauseButton.textContent = paused ? "Resume" : "Pause";
      pauseButton.hidden = false;
      skipButton.hidden = false;
      upNextLabel.textContent = exerciseIndex < cards.length - 1
        ? `UP NEXT · ${cards[exerciseIndex + 1].dataset.exerciseName}`
        : "LAST MOVEMENT · FINISH STRONG";
      updateClock();
      if (announce) {
        if (setIndex === 0) speakExercise(card);
        else speak(card.dataset.exerciseCue);
      }
    };

    const finishWorkout = () => {
      if (timer !== null) window.clearInterval(timer);
      timer = null;
      stopFrames();
      paused = false;
      if (supportsVoice) window.speechSynthesis.cancel();
      phase = "complete";
      player.classList.remove("is-resting");
      exerciseName.textContent = "Workout complete";
      exerciseCue.textContent = "That’s the session done. Take a moment, catch your breath, and be proud you showed up.";
      setLabel.textContent = `${checks.filter((check) => check.checked).length} of ${cards.length} movements completed`;
      clockText.textContent = "✓";
      clockCaption.textContent = "DONE";
      clock.setAttribute("aria-label", "Workout complete");
      timerRing.style.strokeDashoffset = "0";
      timerRing.classList.add("is-done");
      phaseLabel.textContent = "SESSION COMPLETE";
      progressLabel.textContent = `${cards.length} MOVEMENTS`;
      progressSteps.querySelectorAll("span").forEach((step, index) => {
        step.classList.toggle("is-complete", checks[index].checked);
      });
      status.textContent = "Save your completed movements to your training log.";
      upNextLabel.textContent = "SESSION COMPLETE · NICE WORK";
      pauseButton.hidden = true;
      skipButton.hidden = true;
      endButton.hidden = true;
      saveButton.hidden = false;
      exercisePanel.classList.add("is-complete");
      speak("Workout complete. Nice work showing up for yourself.");
    };

    const startTimer = () => {
      if (timer !== null) window.clearInterval(timer);
      timer = window.setInterval(() => {
        if (remaining > 0) remaining -= 1;
        updateClock();
        if (remaining === 5) speak(phase === "work" ? "Five seconds. Keep moving." : "Five seconds. Get ready.");
        if (remaining > 0) return;
        if (phase === "rest") {
          if (!restMovesForward) {
            loadExercise(exerciseIndex, setIndex);
            startTimer();
          } else if (exerciseIndex < cards.length - 1) {
            loadExercise(exerciseIndex + 1);
            startTimer();
          } else {
            finishWorkout();
          }
          return;
        }
        if (phase === "work") {
          const setCount = Number(currentCard().dataset.sets);
          if (setIndex + 1 < setCount) {
            setIndex += 1;
            phase = "rest";
            restMovesForward = false;
          } else {
            checks[exerciseIndex].checked = true;
            checks[exerciseIndex].dispatchEvent(new Event("change", { bubbles: true }));
            if (exerciseIndex >= cards.length - 1) {
              finishWorkout();
              return;
            }
            phase = "rest";
            restMovesForward = true;
          }
          remaining = Number(currentCard().dataset.rest);
          clockCaption.textContent = "REST";
          status.textContent = !restMovesForward
            ? `Rest now. Then repeat set ${setIndex + 1}.`
            : `Rest now. Next up: ${cards[exerciseIndex + 1].dataset.exerciseName}.`;
          if (restMovesForward) {
            const upcoming = cards[exerciseIndex + 1];
            exerciseName.textContent = upcoming.dataset.exerciseName;
            exerciseCue.textContent = upcoming.dataset.exerciseCue;
            setLabel.textContent = `UP NEXT · SET 1 / ${Number(upcoming.dataset.sets)}`;
            animateMovement(upcoming);
          }
          skipButton.hidden = true;
          updateClock();
          speak(status.textContent);
        }
      }, 1000);
    };

    loadExercise(0, 0, false);
    phase = "ready";
    pauseButton.hidden = true;
    skipButton.hidden = true;
    clockText.textContent = formatTime(Number(currentCard().dataset.duration));
    phaseLabel.textContent = "READY WHEN YOU ARE";
    status.textContent = "First, hear a quick introduction to the movement. Your exercise timer will wait until you choose to begin.";

    startButton.addEventListener("click", () => {
      if (phase === "ready") {
        const intro = exerciseIntroduction(currentCard());
        phase = "intro";
        startButton.disabled = true;
        startButton.textContent = "Introducing your exercise…";
        status.textContent = `${intro} Your timer will stay paused until you choose to begin.`;
        player.scrollIntoView({ behavior: "smooth", block: "center" });
        speakExercise(currentCard(), () => {
          if (phase !== "intro") return;
          phase = "intro-ready";
          startButton.disabled = false;
          startButton.innerHTML = "Start exercise <span>▶</span>";
          status.textContent = "That’s the introduction and form cue. Start the exercise whenever you feel ready.";
        });
        return;
      }
      if (phase !== "intro-ready") return;
      phase = "work";
      remaining = Number(currentCard().dataset.duration);
      startButton.hidden = true;
      pauseButton.hidden = false;
      skipButton.hidden = false;
      endButton.hidden = false;
      status.textContent = "Move at a comfortable pace. Modify the movement if you need to.";
      updateClock();
      startTimer();
    });

    pauseButton.addEventListener("click", () => {
      if (paused) {
        paused = false;
        pauseButton.textContent = "Pause";
        status.textContent = phase === "work" ? "Session resumed. Keep moving comfortably." : "Rest timer resumed.";
        speak(status.textContent);
        startTimer();
        return;
      }
      paused = true;
      if (timer !== null) window.clearInterval(timer);
      timer = null;
      if (supportsVoice) window.speechSynthesis.cancel();
      pauseButton.textContent = "Resume";
      status.textContent = "Paused. Resume when you are ready.";
    });

    skipButton.addEventListener("click", () => {
      if (exerciseIndex >= cards.length - 1) return;
      loadExercise(exerciseIndex + 1, 0);
      if (!paused) startTimer();
    });

    endButton.addEventListener("click", () => {
      if (!window.confirm("End this session? Your completed movements will not be saved unless you finish the workout.")) return;
      if (timer !== null) window.clearInterval(timer);
      timer = null;
      stopFrames();
      if (supportsVoice) window.speechSynthesis.cancel();
      endButton.hidden = true;
      startButton.hidden = false;
      pauseButton.hidden = true;
      skipButton.hidden = true;
      saveButton.hidden = true;
      phase = "ready";
      introSequence += 1;
      paused = false;
      restMovesForward = false;
      exerciseIndex = 0;
      setIndex = 0;
      timerRing.classList.remove("is-done");
      exercisePanel.classList.remove("is-complete");
      loadExercise(0, 0, false);
      phase = "ready";
      pauseButton.hidden = true;
      skipButton.hidden = true;
      clockText.textContent = formatTime(Number(currentCard().dataset.duration));
      phaseLabel.textContent = "READY WHEN YOU ARE";
      startButton.disabled = false;
      startButton.innerHTML = "Tell me about this exercise <span>◖</span>";
      status.textContent = "First, hear a quick introduction to the movement. Your exercise timer will wait until you choose to begin.";
      checks.forEach((check) => {
        check.checked = false;
        check.dispatchEvent(new Event("change", { bubbles: true }));
      });
    });

    voiceButton.addEventListener("click", () => {
      voiceEnabled = !voiceEnabled && supportsVoice;
      voiceButton.setAttribute("aria-pressed", String(voiceEnabled));
      voiceButton.textContent = voiceEnabled ? "Voice on" : "Voice off";
      if (!voiceEnabled && supportsVoice) window.speechSynthesis.cancel();
      if (phase === "intro") {
        if (voiceEnabled) {
          speakExercise(currentCard(), () => {
            if (phase !== "intro") return;
            phase = "intro-ready";
            startButton.disabled = false;
            startButton.innerHTML = "Start exercise <span>▶</span>";
            status.textContent = "That’s the introduction and form cue. Start the exercise whenever you feel ready.";
          });
        } else {
          introSequence += 1;
          phase = "intro-ready";
          startButton.disabled = false;
          startButton.innerHTML = "Start exercise <span>▶</span>";
          status.textContent = `${exerciseIntroduction(currentCard())} Start the exercise whenever you're ready.`;
        }
      } else if (voiceEnabled && phase === "work") {
        speak(currentCard().dataset.exerciseCue);
      }
    });
    if (!supportsVoice) {
      voiceButton.disabled = true;
      voiceButton.innerHTML = "<span aria-hidden=\"true\">◖</span> Voice unavailable";
      voiceButton.setAttribute("aria-pressed", "false");
    }
  }

  let restTimer = null;
  let activeRestButton = null;
  document.querySelectorAll(".rest-button").forEach((button) => {
    button.addEventListener("click", () => {
      if (restTimer !== null) window.clearInterval(restTimer);
      if (activeRestButton) {
        activeRestButton.disabled = false;
        activeRestButton.innerHTML = `⏱ <span>Rest ${activeRestButton.dataset.seconds}s</span>`;
      }
      let remaining = Number(button.dataset.seconds);
      if (!Number.isFinite(remaining) || remaining < 1) return;
      activeRestButton = button;
      button.disabled = true;
      button.innerHTML = `⏱ <span>${remaining}s left</span>`;
      restTimer = window.setInterval(() => {
        remaining -= 1;
        if (remaining <= 0) {
          window.clearInterval(restTimer);
          restTimer = null;
          button.disabled = false;
          button.innerHTML = "✓ <span>Rest complete</span>";
          activeRestButton = null;
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
