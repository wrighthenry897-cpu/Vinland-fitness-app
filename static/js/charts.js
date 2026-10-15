(() => {
  const script = document.getElementById("chart-data");
  if (!script) return;
  let days;
  try {
    days = JSON.parse(script.textContent);
  } catch (error) {
    console.error("Vinland could not read the chart data.", error);
    return;
  }
  const canvas = document.querySelector("#volume-chart, #progress-chart");
  if (!canvas || !Array.isArray(days)) return;
  const isMonth = canvas.id === "progress-chart";
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  function draw() {
    const bounds = canvas.getBoundingClientRect();
    if (!bounds.width || !bounds.height) return;
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.round(bounds.width * ratio);
    canvas.height = Math.round(bounds.height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    ctx.clearRect(0, 0, bounds.width, bounds.height);
    const left = isMonth ? 5 : 6;
    const right = isMonth ? 8 : 6;
    const top = 8;
    const bottom = isMonth ? 15 : 8;
    const width = bounds.width - left - right;
    const height = bounds.height - top - bottom;
    const maxValue = Math.max(1, ...days.map((day) => Number(day.volume) || 0));
    const roundedMax = maxValue === 0 ? 1 : maxValue * 1.12;
    const gridColor = "#eef1ed";
    ctx.lineWidth = 1;
    ctx.font = "9px DM Sans, sans-serif";
    ctx.textBaseline = "middle";

    for (let row = 0; row <= 3; row += 1) {
      const y = top + (height / 3) * row;
      ctx.beginPath();
      ctx.strokeStyle = gridColor;
      ctx.moveTo(left, y);
      ctx.lineTo(bounds.width - right, y);
      ctx.stroke();
      if (isMonth) {
        ctx.fillStyle = "#a1aaa4";
        const value = Math.round(roundedMax * (1 - row / 3));
        ctx.fillText(value >= 1000 ? `${(value / 1000).toFixed(value >= 10000 ? 0 : 1)}k` : String(value), left + 3, y - 8);
      }
    }

    if (isMonth) {
      const gap = width / Math.max(days.length - 1, 1);
      const points = days.map((day, index) => ({
        x: left + index * gap,
        y: top + height - ((Number(day.volume) || 0) / roundedMax) * height,
      }));
      const gradient = ctx.createLinearGradient(0, top, 0, top + height);
      gradient.addColorStop(0, "rgba(176, 218, 126, .27)");
      gradient.addColorStop(1, "rgba(176, 218, 126, 0)");
      ctx.beginPath();
      points.forEach((point, index) => {
        if (index === 0) ctx.moveTo(point.x, point.y);
        else ctx.lineTo(point.x, point.y);
      });
      if (points.length) {
        ctx.lineTo(points[points.length - 1].x, top + height);
        ctx.lineTo(points[0].x, top + height);
      }
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();
      ctx.beginPath();
      points.forEach((point, index) => {
        if (index === 0) ctx.moveTo(point.x, point.y);
        else ctx.lineTo(point.x, point.y);
      });
      ctx.strokeStyle = "#8dbb61";
      ctx.lineWidth = 2;
      ctx.lineJoin = "round";
      ctx.stroke();
      points.forEach((point, index) => {
        if (Number(days[index].volume) > 0) {
          ctx.beginPath();
          ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
          ctx.fillStyle = "#fff";
          ctx.fill();
          ctx.strokeStyle = "#82af58";
          ctx.lineWidth = 1.5;
          ctx.stroke();
        }
      });
    } else {
      const slot = width / days.length;
      const barWidth = Math.min(25, slot * .48);
      days.forEach((day, index) => {
        const value = Number(day.volume) || 0;
        const barHeight = Math.max(value ? 3 : 0, (value / roundedMax) * height);
        const x = left + slot * index + (slot - barWidth) / 2;
        const y = top + height - barHeight;
        const gradient = ctx.createLinearGradient(0, y, 0, top + height);
        gradient.addColorStop(0, "#b9e486");
        gradient.addColorStop(1, "#e5f1d6");
        ctx.beginPath();
        ctx.roundRect(x, y, barWidth, barHeight, [4, 4, 1, 1]);
        ctx.fillStyle = gradient;
        ctx.fill();
        if (day.sessions) {
          ctx.beginPath();
          ctx.arc(x + barWidth / 2, top + height + 3, 2, 0, Math.PI * 2);
          ctx.fillStyle = "#8db75c";
          ctx.fill();
        }
      });
    }
  }

  draw();
  if ("ResizeObserver" in window) new ResizeObserver(draw).observe(canvas.parentElement);
  else window.addEventListener("resize", draw);
})();
