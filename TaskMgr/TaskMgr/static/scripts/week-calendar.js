document.addEventListener("DOMContentLoaded", () => {
  const SESSION_KEY = "taskmgr_session";
  const GROUPS_KEY = "taskmgr_groups";
  const NOTES_PREFIX = "taskmgr_notes_";

  const dayNames = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
  const eventTypeLabels = {
    lesson: "Урок",
    homework: "Домашнее",
    practice: "Практика",
    control: "Контрольная",
    other: "Событие"
  };

  let selectedEventId = null;

  function readJson(key, fallback) {
    try {
      return JSON.parse(localStorage.getItem(key)) ?? fallback;
    } catch {
      return fallback;
    }
  }

  function writeJson(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  function getSession() {
    return readJson(SESSION_KEY, null);
  }

  function getGroups() {
    return readJson(GROUPS_KEY, []);
  }

  function saveGroups(groups) {
    writeJson(GROUPS_KEY, groups);
  }

  function getCurrentGroup() {
    const session = getSession();
    if (!session?.currentGroupId) return null;
    return getGroups().find((group) => group.id === session.currentGroupId) ?? null;
  }

  function updateSession(data) {
    const session = getSession();
    writeJson(SESSION_KEY, { ...session, ...data });
  }

  function getRole(group) {
    const session = getSession();
    if (!session || !group) return "none";
    return group.members?.[session.userId] ?? "none";
  }

  function canManage(group) {
    return getRole(group) === "leader";
  }

  function generateCode() {
    return Math.random().toString(36).slice(2, 8).toUpperCase();
  }

  function openModal(id) {
    document.getElementById(id).hidden = false;
  }

  function closeModals() {
    document.querySelectorAll(".modal").forEach((modal) => {
      modal.hidden = true;
    });
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function clearAuth() {
    localStorage.removeItem("taskmgr_session");
    localStorage.removeItem("isAuth");
    localStorage.removeItem("username");
    localStorage.removeItem("userRole");
    localStorage.removeItem("rememberMe");
    sessionStorage.removeItem("tempAuth");
  }

  function requireAuth() {
    const session = getSession();
    const isAuth = localStorage.getItem("isAuth") === "true";
    if (!session || !isAuth) {
      window.location.replace("/");
      return null;
    }

    if (session.remember === false && sessionStorage.getItem("tempAuth") !== "true") {
      clearAuth();
      window.location.replace("/");
      return null;
    }

    return session;
  }

  function renderProfile() {
    const session = getSession();
    document.getElementById("profile-name").textContent = session.displayName || session.username;
    document.getElementById("profile-login").textContent = `@${session.username}`;
    document.getElementById("profile-avatar").textContent = (session.displayName || session.username || "T").slice(0, 1).toUpperCase();

    const notes = document.getElementById("notes-input");
    notes.value = localStorage.getItem(`${NOTES_PREFIX}${session.userId}`) ?? "";
  }

  function renderGroup() {
    const group = getCurrentGroup();
    const card = document.getElementById("current-group-card");
    const rolePill = document.getElementById("role-pill");
    const title = document.getElementById("workspace-title");
    const empty = document.getElementById("empty-state");
    const calendar = document.getElementById("calendar-panel");
    const addButton = document.getElementById("add-event-button");

    if (!group) {
      card.innerHTML = `
        <strong>Группа не выбрана</strong>
        <span>Создайте группу или присоединитесь по коду.</span>
      `;
      rolePill.textContent = "Без группы";
      delete rolePill.dataset.role;
      title.textContent = "Расписание и события недели";
      empty.hidden = false;
      calendar.hidden = true;
      renderDetails(null);
      return;
    }

    const role = getRole(group);
    const isLeader = role === "leader";
    const membersCount = Object.keys(group.members ?? {}).length;

    card.innerHTML = `
      <strong>${escapeHtml(group.name)}</strong>
      <span>Код: <b>${escapeHtml(group.code)}</b></span>
      <span>${membersCount} участник(а)</span>
    `;
    rolePill.textContent = isLeader ? "Староста" : "Ученик";
    rolePill.dataset.role = role;
    title.textContent = group.name;
    empty.hidden = true;
    calendar.hidden = false;
    addButton.hidden = !isLeader;
    renderWeek(group);
    renderDetails(selectedEventId);
  }

  function renderWeek(group) {
    const grid = document.getElementById("week-grid");
    const events = group.events ?? [];

    grid.innerHTML = dayNames.map((name, dayIndex) => {
      const dayEvents = events
        .filter((event) => Number(event.day) === dayIndex)
        .sort((a, b) => (a.time || "").localeCompare(b.time || ""));

      return `
        <section class="day-column">
          <div class="day-column__head">
            <span>${name}</span>
            <strong>${dayIndex + 1}</strong>
          </div>
          <div class="day-column__events">
            ${dayEvents.length ? dayEvents.map(renderEventButton).join("") : '<p class="day-empty">Нет событий</p>'}
          </div>
        </section>
      `;
    }).join("");
  }

  function renderEventButton(event) {
    return `
      <button class="event-card ${selectedEventId === event.id ? "event-card--active" : ""}" type="button" data-event-id="${event.id}">
        <span class="event-card__type">${eventTypeLabels[event.type] ?? "Событие"}</span>
        <strong>${escapeHtml(event.title)}</strong>
        <span>${event.time || "Без времени"}</span>
      </button>
    `;
  }

  function findSelectedEvent(group, eventId) {
    if (!group || !eventId) return null;
    return (group.events ?? []).find((event) => event.id === eventId) ?? null;
  }

  function renderDetails(eventId) {
    const body = document.getElementById("details-body");
    const group = getCurrentGroup();
    const event = findSelectedEvent(group, eventId);
    const isLeader = canManage(group);

    if (!group) {
      body.innerHTML = '<p class="muted">Создайте группу или присоединитесь к существующей.</p>';
      return;
    }

    if (!event) {
      body.innerHTML = `
        <p class="muted">Выберите событие в расписании, чтобы посмотреть детали и комментарии.</p>
        <div class="rights-box">
          <strong>Права роли</strong>
          <span>${isLeader ? "Староста может создавать и редактировать расписание, домашние задания и события." : "Ученик может смотреть расписание и оставлять комментарии."}</span>
        </div>
      `;
      return;
    }

    const comments = event.comments ?? [];
    body.innerHTML = `
      <article class="detail-event">
        <span class="event-card__type">${eventTypeLabels[event.type] ?? "Событие"}</span>
        <h2>${escapeHtml(event.title)}</h2>
        <p>${dayNames[event.day]} ${event.time ? `• ${escapeHtml(event.time)}` : ""}</p>
        <div class="description">${escapeHtml(event.description || "Описание не добавлено.")}</div>
        ${isLeader ? '<button class="action-btn" type="button" id="edit-event-button">Редактировать</button>' : ""}
      </article>

      <section class="comments">
        <h3>Комментарии</h3>
        <div class="comment-list">
          ${comments.length ? comments.map((comment) => `
            <div class="comment">
              <strong>${escapeHtml(comment.author)}</strong>
              <span>${escapeHtml(comment.text)}</span>
            </div>
          `).join("") : '<p class="muted">Комментариев пока нет.</p>'}
        </div>
        <form class="comment-form" id="comment-form">
          <textarea class="input input--textarea" id="comment-text" placeholder="Оставить комментарий"></textarea>
          <button class="primary-btn" type="submit">Отправить</button>
        </form>
      </section>
    `;
  }

  function saveGroupEvent(eventData) {
    const session = getSession();
    const groups = getGroups();
    const group = groups.find((item) => item.id === session.currentGroupId);
    if (!group || !canManage(group)) return;

    group.events ??= [];
    const existing = group.events.find((event) => event.id === eventData.id);

    if (existing) {
      Object.assign(existing, eventData);
    } else {
      group.events.push(eventData);
    }

    saveGroups(groups);
    selectedEventId = eventData.id;
    renderGroup();
  }

  function openEventForm(event = null) {
    const isEdit = Boolean(event);
    document.getElementById("event-form-title").textContent = isEdit ? "Редактировать событие" : "Добавить событие";
    document.getElementById("event-id").value = event?.id ?? "";
    document.getElementById("event-type").value = event?.type ?? "lesson";
    document.getElementById("event-day").value = String(event?.day ?? 0);
    document.getElementById("event-time").value = event?.time ?? "";
    document.getElementById("event-title").value = event?.title ?? "";
    document.getElementById("event-description").value = event?.description ?? "";
    openModal("event-modal");
  }

  const session = requireAuth();
  if (!session) return;

  renderProfile();
  renderGroup();

  document.getElementById("logout-button").addEventListener("click", () => {
    clearAuth();
    window.location.replace("/");
  });

  document.getElementById("notes-input").addEventListener("input", (event) => {
    localStorage.setItem(`${NOTES_PREFIX}${getSession().userId}`, event.target.value);
  });

  document.getElementById("create-group-button").addEventListener("click", () => openModal("group-modal"));
  document.getElementById("join-group-button").addEventListener("click", () => openModal("join-modal"));
  document.getElementById("add-event-button").addEventListener("click", () => {
    if (canManage(getCurrentGroup())) openEventForm();
  });

  document.addEventListener("click", (event) => {
    if (event.target.matches("[data-close-modal]") || event.target.classList.contains("modal")) {
      closeModals();
    }

    const eventButton = event.target.closest("[data-event-id]");
    if (eventButton) {
      selectedEventId = eventButton.dataset.eventId;
      renderGroup();
    }

    if (event.target.id === "edit-event-button") {
      const group = getCurrentGroup();
      const eventToEdit = findSelectedEvent(group, selectedEventId);
      if (eventToEdit && canManage(group)) openEventForm(eventToEdit);
    }
  });

  document.getElementById("group-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const name = document.getElementById("group-name").value.trim();
    if (!name) return;

    const session = getSession();
    const groups = getGroups();
    const group = {
      id: `group-${Date.now()}`,
      name,
      code: generateCode(),
      createdBy: session.userId,
      members: { [session.userId]: "leader" },
      events: [
        {
          id: `event-${Date.now()}`,
          type: "lesson",
          day: 0,
          time: "09:00",
          title: "Первое занятие",
          description: "Староста может изменить это событие или добавить новые.",
          comments: []
        }
      ]
    };

    groups.push(group);
    saveGroups(groups);
    updateSession({ currentGroupId: group.id });
    document.getElementById("group-name").value = "";
    closeModals();
    renderGroup();
  });

  document.getElementById("join-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const code = document.getElementById("join-code").value.trim().toUpperCase();
    const groups = getGroups();
    const session = getSession();
    const group = groups.find((item) => item.code === code);

    if (!group) {
      document.getElementById("join-message").textContent = "Группа с таким кодом не найдена.";
      return;
    }

    group.members ??= {};
    group.members[session.userId] ??= "member";
    saveGroups(groups);
    updateSession({ currentGroupId: group.id });
    document.getElementById("join-code").value = "";
    document.getElementById("join-message").textContent = "";
    closeModals();
    renderGroup();
  });

  document.getElementById("event-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const existingId = document.getElementById("event-id").value;
    const group = getCurrentGroup();
    const existing = findSelectedEvent(group, existingId);

    saveGroupEvent({
      id: existingId || `event-${Date.now()}`,
      type: document.getElementById("event-type").value,
      day: Number(document.getElementById("event-day").value),
      time: document.getElementById("event-time").value,
      title: document.getElementById("event-title").value.trim() || "Новое событие",
      description: document.getElementById("event-description").value.trim(),
      comments: existing?.comments ?? []
    });

    closeModals();
  });

  document.addEventListener("submit", (event) => {
    if (event.target.id !== "comment-form") return;
    event.preventDefault();

    const text = document.getElementById("comment-text").value.trim();
    if (!text) return;

    const session = getSession();
    const groups = getGroups();
    const group = groups.find((item) => item.id === session.currentGroupId);
    const item = findSelectedEvent(group, selectedEventId);
    if (!item) return;

    item.comments ??= [];
    item.comments.push({
      id: `comment-${Date.now()}`,
      author: session.displayName || session.username,
      text,
      createdAt: new Date().toISOString()
    });

    saveGroups(groups);
    renderGroup();
  });
});
