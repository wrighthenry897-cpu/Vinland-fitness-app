(() => {
  const DEMO_FRAME_INTERVAL = 2600;
  const PLAYER_FRAME_INTERVAL = 2600;

  const form = document.getElementById("guided-workout-form");
  if (!form) return;

  const dayRail = document.querySelector(".day-rail-scroll");
  const selectedDay = dayRail?.querySelector(".day-rail-link.is-selected");
  if (dayRail && selectedDay) {
    const railBounds = dayRail.getBoundingClientRect();
    const dayBounds = selectedDay.getBoundingClientRect();
    dayRail.scrollLeft += dayBounds.left - railBounds.left
      - (dayRail.clientWidth - selectedDay.clientWidth) / 2;
  }

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
    const frameNumber = frameCount.querySelector(".demo-frame-number");
    const frameLabel = frameCount.querySelector(".demo-frame-label");
    const frames = [photo.getAttribute("src"), photo.dataset.nextFrame];
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const transitionPhoto = photo.cloneNode(false);
    transitionPhoto.classList.add("exercise-demo-transition");
    transitionPhoto.src = frames[1];
    transitionPhoto.alt = "";
    transitionPhoto.setAttribute("aria-hidden", "true");
    canvas.append(transitionPhoto);
    let currentFrame = 0;
    let timer = null;

    const showFrame = (index) => {
      currentFrame = index;
      photo.dataset.currentFrame = String(index);
      frameNumber.textContent = `0${index + 1}`;
      frameLabel.textContent = index === 0 ? photo.dataset.firstLabel : photo.dataset.secondLabel;
      photo.alt = `${photo.dataset.exerciseName} ${index === 0 ? photo.dataset.firstPosition : photo.dataset.secondPosition} position`;
      step.setAttribute("aria-label", `Show the ${index === 0 ? "finishing" : "starting"} position`);
      transitionPhoto.classList.toggle("is-visible", index === 1);
    };

    const advanceFrame = () => showFrame(currentFrame === 0 ? 1 : 0);

    const pause = () => {
      if (timer !== null) window.clearInterval(timer);
      timer = null;
      toggle.setAttribute("aria-pressed", "true");
      toggle.setAttribute("aria-label", "Play movement demo");
      toggle.title = "Play movement demo";
      toggle.textContent = "▶";
    };

    const play = () => {
      if (timer !== null) return;
      toggle.setAttribute("aria-pressed", "false");
      toggle.setAttribute("aria-label", "Pause movement demo");
      toggle.title = "Pause movement demo";
      toggle.textContent = "Ⅱ";
      timer = window.setInterval(advanceFrame, DEMO_FRAME_INTERVAL);
    };

    step.addEventListener("click", advanceFrame);
    toggle.addEventListener("click", () => {
      if (timer === null) play();
      else pause();
    });
    showFrame(0);
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
    const voiceSelect = document.getElementById("coach-voice-select");
    const styleSelect = document.getElementById("coach-style-select");
    const speedSelect = document.getElementById("coach-speed-select");
    const endButton = document.getElementById("workout-end");
    const saveButton = document.getElementById("workout-save");
    const supportsVoice = "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
    const voiceStorageKey = "vinland-coach-voice";
    const deliveryStyles = {
      balanced: { rate: 0.95, pitch: 1 },
      calm: { rate: 0.9, pitch: 0.96 },
      upbeat: { rate: 1, pitch: 1.05 },
    };
    let voicePreferences = { voiceURI: "", style: "balanced", speed: "1" };
    try {
      const savedPreferences = JSON.parse(window.localStorage.getItem(voiceStorageKey) || "{}");
      voicePreferences = { ...voicePreferences, ...savedPreferences };
    } catch (error) {
      console.warn("Could not load saved coach voice preferences.", error);
    }
    const circumference = 2 * Math.PI * 78;
    let exerciseIndex = 0;
    let setIndex = 0;
    let remaining = 0;
    let phase = "ready";
    let timer = null;
    let voiceEnabled = supportsVoice;
    let paused = false;
    let frameTimer = null;
    let playerFrame = 0;
    let restMovesForward = false;
    let introSequence = 0;

    const saveVoicePreferences = () => {
      voicePreferences.voiceURI = voiceSelect.value;
      voicePreferences.style = styleSelect.value;
      voicePreferences.speed = speedSelect.value;
      try {
        window.localStorage.setItem(voiceStorageKey, JSON.stringify(voicePreferences));
      } catch (error) {
        console.warn("Could not save coach voice preferences.", error);
      }
    };

    const availableVoices = () => window.speechSynthesis.getVoices();
    const preferredVoice = () => {
      const voices = availableVoices();
      const englishVoices = voices.filter((voice) => voice.lang.toLowerCase().startsWith("en"));
      const naturalVoice = englishVoices.find((voice) => {
        const name = voice.name.toLowerCase();
        return name.includes("natural") || name.includes("enhanced") || name.includes("premium");
      });
      return voices.find((voice) => voice.voiceURI === voiceSelect.value)
        || naturalVoice
        || englishVoices.find((voice) => voice.default)
        || englishVoices[0]
        || voices.find((voice) => voice.default)
        || voices[0]
        || null;
    };

    const populateVoiceOptions = () => {
      const voices = availableVoices().sort((first, second) => {
        const score = (voice) => {
          const name = voice.name.toLowerCase();
          return (voice.lang.toLowerCase().startsWith("en") ? 0 : 10)
            + (name.includes("natural") || name.includes("enhanced") ? 0 : 1)
            + (voice.default ? -1 : 0);
        };
        return score(first) - score(second) || first.name.localeCompare(second.name);
      });
      const selectedVoice = voicePreferences.voiceURI;
      voiceSelect.replaceChildren(new Option("Recommended available voice", ""));
      voices.forEach((voice) => {
        const option = new Option(`${voice.name} (${voice.lang})`, voice.voiceURI);
        voiceSelect.add(option);
      });
      voiceSelect.value = voices.some((voice) => voice.voiceURI === selectedVoice) ? selectedVoice : "";
    };

    if (supportsVoice) {
      styleSelect.value = deliveryStyles[voicePreferences.style] ? voicePreferences.style : "balanced";
      speedSelect.value = ["0.85", "1", "1.15"].includes(voicePreferences.speed) ? voicePreferences.speed : "1";
      populateVoiceOptions();
      window.speechSynthesis.addEventListener("voiceschanged", populateVoiceOptions);
      [voiceSelect, styleSelect, speedSelect].forEach((select) => {
        select.addEventListener("change", saveVoicePreferences);
      });
    } else {
      voiceSelect.disabled = true;
      styleSelect.disabled = true;
      speedSelect.disabled = true;
    }

    const speak = (message) => {
      if (!voiceEnabled) return;
      window.speechSynthesis.cancel();
      const instruction = new SpeechSynthesisUtterance(message);
      const style = deliveryStyles[styleSelect.value] || deliveryStyles.balanced;
      instruction.voice = preferredVoice();
      instruction.rate = style.rate * Number(speedSelect.value);
      instruction.pitch = style.pitch;
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
      const style = deliveryStyles[styleSelect.value] || deliveryStyles.balanced;
      [intro, cue].forEach((instruction) => {
        instruction.voice = preferredVoice();
        instruction.rate = style.rate * Number(speedSelect.value);
        instruction.pitch = style.pitch;
      });
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
      nextDemoImage.src = endFrame;
      nextDemoImage.classList.remove("is-current");
      playerFrame = 0;
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (startFrame === endFrame || reducedMotion) return;
      frameTimer = window.setInterval(() => {
        playerFrame = playerFrame === 0 ? 1 : 0;
        demoImage.classList.toggle("is-current", playerFrame === 0);
        nextDemoImage.classList.toggle("is-current", playerFrame === 1);
      }, PLAYER_FRAME_INTERVAL);
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
