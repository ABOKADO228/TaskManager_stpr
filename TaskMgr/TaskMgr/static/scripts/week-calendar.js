console.log("week-calendar.js loaded");

const data = {
    numerator: [
        { weekday: "Пн", number: 1, shift: false, lessons: [
                { title: "Математика", time: "09:00" },
                { title: "Физика", time: "10:40" },
            ]},
        { weekday: "Вт", number: 2, shift: true, lessons: [] },
        { weekday: "Ср", number: 3, shift: false, lessons: [
                { title: "Английский", time: "12:20" },
            ]},
        { weekday: "Чт", number: 4, shift: false, lessons: [] },
        { weekday: "Пт", number: 5, shift: false, lessons: [] },
        { weekday: "Сб", number: 6, shift: false, lessons: [] },
        { weekday: "Вс", number: 7, shift: false, lessons: [] },
    ],
    denominator: [
        { weekday: "Пн", number: 1, shift: false, lessons: [] },
        { weekday: "Вт", number: 2, shift: false, lessons: [
                { title: "История", time: "09:00" },
            ]},
        { weekday: "Ср", number: 3, shift: false, lessons: [] },
        { weekday: "Чт", number: 4, shift: true, lessons: [
                { title: "Программирование", time: "10:40" },
                { title: "Базы данных", time: "12:20" },
            ]},
        { weekday: "Пт", number: 5, shift: false, lessons: [] },
        { weekday: "Сб", number: 6, shift: false, lessons: [] },
        { weekday: "Вс", number: 7, shift: false, lessons: [] },
    ],
};

function lessonBtnHtml(lesson, week, day, idx) {
    return `
    <button type="button" 
    class="lesson-btn"
      data-week="${week}" 
      data-day="${day}" 
      data-lesson="${idx}">
      ${lesson.time ? `<span class="lesson-btn__time">${lesson.time}</span>` : ""}
      <span class="lesson-btn__title">${lesson.title}</span>
    </button>
  `;
}

function dayCardHtml(day, week, dayIndex) {
    const hasLessons = day.lessons && day.lessons.length > 0;

    const lessonsHtml = hasLessons
        ? day.lessons.map((l, i) => lessonBtnHtml(l, week, dayIndex, i)).join("")
        : "";

    return `
    <div class="day-card ${hasLessons ? "" : "day-card--empty"}"
         data-week="${week}" data-day="${dayIndex}">

      <div class="day-card__line day-card__line--top"></div>

      <div class="day-card__header">
        <div class="day-card__weekday">${day.weekday}</div>
        <div class="day-card__number">${day.number}</div>
      </div>

      <div class="day-card__line"></div>

      <div class="day-card__lessons">
        ${lessonsHtml}
        <button class="day-card__add-btn" type="button"
          data-week="${week}" data-day="${dayIndex}">+</button>
      </div>

      <div class="day-card__shift">
        <input type="checkbox" class="day-card__checkbox" ${day.shift ? "checked" : ""} />
        <span class="day-card__shift-label">Замены</span>
      </div>

      <div class="day-card__line day-card__line--bottom"></div>
    </div>
  `;
}

function render(containerId, days, week) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = days.map((d, i) => dayCardHtml(d, week, i)).join("");
}

function rerender() {
    render("numerator-days", data.numerator, "numerator");
    render("denominator-days", data.denominator, "denominator");

    const monthYear = document.getElementById("MonthYearText");
    if (monthYear) monthYear.textContent = "Март 2026";
}

document.addEventListener("click", (e) => {
    const addBtn = e.target.closest(".day-card__add-btn");
    if (addBtn) {
        const week = addBtn.dataset.week;
        const dayIndex = Number(addBtn.dataset.day);
        const list = week === "numerator" ? data.numerator : data.denominator;

        list[dayIndex].lessons.push({ title: "Новый предмет", time: "00:00" });
        rerender();
        return;
    }

    const lessonBtn = e.target.closest(".lesson-btn");
    if (lessonBtn) {
        // Заглушка: потом заменишь на обновление панели "Информация"
        console.log("lesson clicked", {
            week: lessonBtn.dataset.week,
            day: Number(lessonBtn.dataset.day),
            lesson: Number(lessonBtn.dataset.lesson),
        });
    }
});

document.addEventListener("change", (e) => {
    const cb = e.target.closest(".day-card__checkbox");
    if (!cb) return;

    const card = cb.closest(".day-card");
    const week = card.dataset.week;
    const dayIndex = Number(card.dataset.day);
    const list = week === "numerator" ? data.numerator : data.denominator;

    list[dayIndex].shift = cb.checked;
});

window.addEventListener("DOMContentLoaded", rerender);