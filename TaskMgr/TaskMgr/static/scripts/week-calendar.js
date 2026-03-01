// static/scripts/week-calendar.js
console.log("week-calendar.js loaded");

const data = {
    numerator: [
        {
            weekday: "Пн", number: 1, shift: false, lessons: [
                { id: "m1", title: "Математика", time: "09:00" },
                { id: "p1", title: "Физика", time: "10:40" },
            ]
        },
        { weekday: "Вт", number: 2, shift: true, lessons: [] },
        {
            weekday: "Ср", number: 3, shift: false, lessons: [
                { id: "e1", title: "Английский", time: "12:20" },
            ]
        },
        { weekday: "Чт", number: 4, shift: false, lessons: [] },
        { weekday: "Пт", number: 5, shift: false, lessons: [] },
        { weekday: "Сб", number: 6, shift: false, lessons: [] },
        { weekday: "Вс", number: 7, shift: false, lessons: [] },
    ],
    denominator: [
        { weekday: "Пн", number: 1, shift: false, lessons: [] },
        {
            weekday: "Вт", number: 2, shift: false, lessons: [
                { id: "h1", title: "История", time: "09:00" },
            ]
        },
        { weekday: "Ср", number: 3, shift: false, lessons: [] },
        {
            weekday: "Чт", number: 4, shift: true, lessons: [
                { id: "pr1", title: "Программирование", time: "10:40" },
                { id: "db1", title: "Базы данных", time: "12:20" },
            ]
        },
        { weekday: "Пт", number: 5, shift: false, lessons: [] },
        { weekday: "Сб", number: 6, shift: false, lessons: [] },
        { weekday: "Вс", number: 7, shift: false, lessons: [] },
    ],
};

function escapeHtml(s) {
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

// Урок = кнопка
function renderLessonButton(lesson, weekType, dayIndex, lessonIndex) {
    const time = lesson.time ? `<span class="lesson-btn__time">${escapeHtml(lesson.time)}</span>` : "";
    return `
    <button
      type="button"
      class="lesson-btn"
      data-week="${weekType}"
      data-day="${dayIndex}"
      data-lesson="${lessonIndex}"
    >
      ${time}
      <span class="lesson-btn__title">${escapeHtml(lesson.title)}</span>
    </button>
  `;
}

function renderDayCard(day, weekType, dayIndex) {
    const hasLessons = day.lessons && day.lessons.length > 0;

    const lessonsButtons = hasLessons
        ? day.lessons.map((l, i) => renderLessonButton(l, weekType, dayIndex, i)).join("")
        : "";

    // "+" ВСЕГДА в конце. Если уроков нет — будет единственной кнопкой (и CSS центрирует)
    const plusBtn = `
    <button class="day-card__add-btn" type="button" data-week="${weekType}" data-day="${dayIndex}">+</button>
  `;

    return `
    <div class="day-card ${hasLessons ? "" : "day-card--empty"}" data-week="${weekType}" data-day="${dayIndex}">
      <div class="day-card__line day-card__line--top"></div>

      <div class="day-card__header">
        <div class="day-card__weekday">${escapeHtml(day.weekday)}</div>
        <div class="day-card__number">${escapeHtml(day.number)}</div>
      </div>

      <div class="day-card__line"></div>

      <div class="day-card__lessons">
        ${lessonsButtons}
        ${plusBtn}
      </div>

      <div class="day-card__shift">
        <input type="checkbox" class="day-card__checkbox" ${day.shift ? "checked" : ""} />
        <span class="day-card__shift-label">Замены</span>
      </div>

      <div class="day-card__line day-card__line--bottom"></div>
    </div>
  `;
}

function renderWeek(containerId, days, weekType) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = days.map((day, idx) => renderDayCard(day, weekType, idx)).join("");
}

function setInfoPanel(text) {
    const ph = document.getElementById("placeHolderText");
    const box = document.getElementById("ucInformation");
    if (!ph || !box) return;

    ph.style.display = "none";
    box.style.display = "block";
    box.textContent = text; // тут потом заменишь на нормальную разметку/данные
}

function rerender() {
    renderWeek("numerator-days", data.numerator, "numerator");
    renderWeek("denominator-days", data.denominator, "denominator");

    const monthYear = document.getElementById("MonthYearText");
    if (monthYear) monthYear.textContent = "Март 2026";
}

function wireEvents() {
    document.addEventListener("click", (e) => {
        // Клик по уроку
        const lessonBtn = e.target.closest(".lesson-btn");
        if (lessonBtn) {
            const week = lessonBtn.dataset.week;
            const dayIndex = Number(lessonBtn.dataset.day);
            const lessonIndex = Number(lessonBtn.dataset.lesson);

            const list = week === "numerator" ? data.numerator : data.denominator;
            const lesson = list[dayIndex].lessons[lessonIndex];

            setInfoPanel(`Выбран предмет: ${lesson.title} (${lesson.time ?? ""})`);
            return;
        }

        // Клик по "+"
        const addBtn = e.target.closest(".day-card__add-btn");
        if (addBtn) {
            const week = addBtn.dataset.week;
            const dayIndex = Number(addBtn.dataset.day);

            const list = week === "numerator" ? data.numerator : data.denominator;

            // демо-добавление: новый предмет-кнопка
            list[dayIndex].lessons.push({
                id: crypto?.randomUUID?.() ?? String(Date.now()),
                title: "Новый предмет",
                time: "00:00"
            });

            rerender();
            return;
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
}

window.addEventListener("DOMContentLoaded", () => {
    wireEvents();
    rerender();
});