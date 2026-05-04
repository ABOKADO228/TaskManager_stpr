<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>TaskMgr - группа и расписание</title>
  <link rel="stylesheet" href="/static/content/css/main/main.css" />
</head>

<body>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="profile">
        <div class="profile__avatar" id="profile-avatar">T</div>
        <div>
          <div class="profile__name" id="profile-name">Пользователь</div>
          <div class="profile__meta" id="profile-login">@user</div>
        </div>
      </div>

      <section class="side-section">
        <div class="side-section__title">Моя группа</div>
        <div class="group-card" id="current-group-card">
          <strong>Группа не выбрана</strong>
          <span>Создайте группу или присоединитесь по коду.</span>
        </div>
        <div class="side-actions">
          <button class="action-btn" type="button" id="create-group-button">Создать группу</button>
          <button class="action-btn action-btn--ghost" type="button" id="join-group-button">Войти по коду</button>
        </div>
      </section>

      <section class="side-section">
        <div class="side-section__title">Заметки</div>
        <textarea class="notes-input" id="notes-input" placeholder="Личные заметки по учебе"></textarea>
      </section>

      <button class="logout-btn" type="button" id="logout-button">Выйти</button>
    </aside>

    <main class="workspace">
      <header class="topline">
        <div>
          <p class="eyebrow">Рабочее пространство группы</p>
          <h1 id="workspace-title">Расписание и события недели</h1>
        </div>
        <div class="role-pill" id="role-pill">Участник</div>
      </header>

      <section class="empty-state" id="empty-state">
        <div>
          <h2>Начните с группы</h2>
          <p>Староста создает группу и получает код. Остальные ученики присоединяются по этому коду и видят общее расписание.</p>
        </div>
      </section>

      <section class="calendar-panel" id="calendar-panel" hidden>
        <div class="calendar-toolbar">
          <div>
            <span class="toolbar-label">Неделя</span>
            <strong id="week-title">Май 2026</strong>
          </div>
          <button class="primary-btn" type="button" id="add-event-button">Добавить событие</button>
        </div>

        <div class="week-grid" id="week-grid"></div>
      </section>
    </main>

    <aside class="details-panel">
      <div class="panel-header">Информация</div>
      <div class="details-body" id="details-body">
        <p class="muted">Выберите событие в расписании, чтобы посмотреть детали и комментарии.</p>
      </div>
    </aside>
  </div>

  <div class="modal" id="group-modal" hidden>
    <form class="modal__card" id="group-form">
      <button class="modal__close" type="button" data-close-modal>×</button>
      <h2>Создать группу</h2>
      <label class="field">
        <span>Название группы</span>
        <input class="input" id="group-name" type="text" placeholder="Например, ИС-21" />
      </label>
      <button class="primary-btn" type="submit">Создать и стать старостой</button>
    </form>
  </div>

  <div class="modal" id="join-modal" hidden>
    <form class="modal__card" id="join-form">
      <button class="modal__close" type="button" data-close-modal>×</button>
      <h2>Присоединиться к группе</h2>
      <label class="field">
        <span>Код группы</span>
        <input class="input" id="join-code" type="text" placeholder="Например, AB12CD" />
      </label>
      <button class="primary-btn" type="submit">Войти как ученик</button>
      <p class="form-message" id="join-message"></p>
    </form>
  </div>

  <div class="modal" id="event-modal" hidden>
    <form class="modal__card modal__card--wide" id="event-form">
      <button class="modal__close" type="button" data-close-modal>×</button>
      <h2 id="event-form-title">Добавить событие</h2>
      <input id="event-id" type="hidden" />

      <div class="form-grid">
        <label class="field">
          <span>Тип</span>
          <select class="input" id="event-type">
            <option value="lesson">Пара / урок</option>
            <option value="homework">Домашнее задание</option>
            <option value="practice">Практическая работа</option>
            <option value="control">Контрольная</option>
            <option value="other">Другое событие</option>
          </select>
        </label>

        <label class="field">
          <span>День недели</span>
          <select class="input" id="event-day">
            <option value="0">Понедельник</option>
            <option value="1">Вторник</option>
            <option value="2">Среда</option>
            <option value="3">Четверг</option>
            <option value="4">Пятница</option>
            <option value="5">Суббота</option>
            <option value="6">Воскресенье</option>
          </select>
        </label>

        <label class="field">
          <span>Время</span>
          <input class="input" id="event-time" type="time" />
        </label>

        <label class="field">
          <span>Название</span>
          <input class="input" id="event-title" type="text" placeholder="Математика, доклад, лабораторная" />
        </label>
      </div>

      <label class="field">
        <span>Описание</span>
        <textarea class="input input--textarea" id="event-description" placeholder="Что нужно подготовить, где пройдет занятие, важные детали"></textarea>
      </label>

      <button class="primary-btn" type="submit">Сохранить</button>
    </form>
  </div>

  <script src="/static/scripts/week-calendar.js"></script>
</body>
</html>
