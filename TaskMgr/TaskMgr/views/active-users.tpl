<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>TaskMgr - активные пользователи</title>
  <link rel="stylesheet" href="/static/content/css/active-users/active-users.css" />
</head>
<body>
  <header class="users-header">
    <div class="users-container users-header__inner">
      <a class="users-logo" href="/">
        <span class="users-logo__mark">T</span>
        <span>TaskMgr</span>
      </a>

      <nav class="users-nav" aria-label="Основная навигация">
        <a href="/main">Расписание</a>
        <a href="/orders">Заказы</a>
        <a class="active" href="/active-users">Активные пользователи</a>
        <a href="/reg-auth">Вход</a>
      </nav>
    </div>
  </header>

  <main class="users-container users-page">
    <section class="users-hero">
      <div>
        <p class="users-eyebrow">Вариант 6</p>
        <h1>Активные пользователи</h1>
        <p>
          Пользователь попадает в список, если набирает достаточно баллов активности.
          Рейтинг считается по событиям, комментариям, заметкам, группам и дате последней активности.
        </p>
      </div>
      <div class="users-count">
        <strong>{{len(users)}}</strong>
        <span>пользователей</span>
      </div>
    </section>

    % if saved:
      <div class="page-notice page-notice--success">Пользователь добавлен. Если рейтинг высокий, он появится в списке активных.</div>
    % end

    <section class="users-layout">
      <form class="user-form" action="/active-users" method="post" novalidate>
        <div class="section-title">
          <span>Новая запись</span>
          <h2>Добавить пользователя</h2>
        </div>

        <label class="field">
          <span>Ник</span>
          <input
            type="text"
            name="nick"
            value="{{form.get('nick', '')}}"
            placeholder="student_leader"
            autocomplete="off"
            required
          />
          % if errors.get("nick"):
            <small class="field-error">{{errors["nick"]}}</small>
          % end
        </label>

        <label class="field">
          <span>Описание активности</span>
          <textarea
            name="description"
            placeholder="Опишите вклад пользователя в работу группы"
            required
          >{{form.get('description', '')}}</textarea>
          % if errors.get("description"):
            <small class="field-error">{{errors["description"]}}</small>
          % end
        </label>

        <div class="form-grid">
          <label class="field">
            <span>Дата активности</span>
            <input
              type="date"
              name="active_date"
              value="{{form.get('active_date', '')}}"
              max="{{today}}"
              required
            />
            % if errors.get("active_date"):
              <small class="field-error">{{errors["active_date"]}}</small>
            % end
          </label>

          <label class="field">
            <span>Телефон</span>
            <input
              type="tel"
              name="phone"
              value="{{form.get('phone', '')}}"
              placeholder="+7 (999) 123-45-67"
              required
            />
            % if errors.get("phone"):
              <small class="field-error">{{errors["phone"]}}</small>
            % end
          </label>
        </div>

        <div class="metric-grid">
          <label class="field">
            <span>Создано событий</span>
            <input type="number" name="events_created" min="0" value="{{form.get('events_created', '0')}}" required />
            % if errors.get("events_created"):
              <small class="field-error">{{errors["events_created"]}}</small>
            % end
          </label>

          <label class="field">
            <span>Комментариев</span>
            <input type="number" name="comments_count" min="0" value="{{form.get('comments_count', '0')}}" required />
            % if errors.get("comments_count"):
              <small class="field-error">{{errors["comments_count"]}}</small>
            % end
          </label>

          <label class="field">
            <span>Заметок</span>
            <input type="number" name="notes_count" min="0" value="{{form.get('notes_count', '0')}}" required />
            % if errors.get("notes_count"):
              <small class="field-error">{{errors["notes_count"]}}</small>
            % end
          </label>

          <label class="field">
            <span>Групп</span>
            <input type="number" name="groups_joined" min="0" value="{{form.get('groups_joined', '0')}}" required />
            % if errors.get("groups_joined"):
              <small class="field-error">{{errors["groups_joined"]}}</small>
            % end
          </label>
        </div>

        <div class="score-preview" aria-live="polite">
          <span>Предварительный рейтинг</span>
          <strong id="score-preview">0</strong>
        </div>

        % if errors:
          <div class="form-alert">
            Проверьте введенные данные. Значения сохранены, исправьте ошибки и повторите отправку.
          </div>
        % end

        <div class="form-actions">
          <button class="submit-button" type="submit">Добавить пользователя</button>
          <button class="ghost-button" type="reset">Очистить</button>
        </div>
      </form>

      <section class="users-list" aria-label="Список активных пользователей">
        <div class="section-title">
          <span>Сортировка: рейтинг сверху</span>
          <h2>Перечень пользователей</h2>
        </div>

        <div class="list-toolbar">
          <label class="search-field">
            <span>Поиск</span>
            <input type="search" id="users-search" placeholder="Ник, описание, телефон или метрика" />
          </label>
        </div>

        % if users:
          <div class="user-cards" id="users-list">
            % for user in users:
              <article class="user-card" data-search="{{user['nick']}} {{user['description']}} {{user['phone']}} {{user.get('events_created', 0)}} {{user.get('comments_count', 0)}} {{user.get('notes_count', 0)}} {{user.get('groups_joined', 0)}}">
                <div class="user-card__top">
                  <span class="user-nick">@{{user["nick"]}}</span>
                  <time datetime="{{user['active_date']}}">{{user["active_date"]}}</time>
                </div>
                <div class="activity-score">
                  <strong>{{user["activity_score"]}}</strong>
                  <span>баллов активности</span>
                </div>
                <p>{{user["description"]}}</p>
                <div class="activity-metrics">
                  <span>События: {{user.get("events_created", 0)}}</span>
                  <span>Комментарии: {{user.get("comments_count", 0)}}</span>
                  <span>Заметки: {{user.get("notes_count", 0)}}</span>
                  <span>Группы: {{user.get("groups_joined", 0)}}</span>
                </div>
                <a class="phone-link" href="tel:{{user['phone']}}">{{user["phone"]}}</a>
              </article>
            % end
          </div>
          <div class="empty-users is-hidden" id="users-empty-search">По такому запросу пользователей не найдено.</div>
        % else:
          <div class="empty-users">Пока нет пользователей, которые прошли порог активности.</div>
        % end
      </section>
    </section>
  </main>

  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const search = document.getElementById("users-search");
      const cards = Array.from(document.querySelectorAll(".user-card"));
      const empty = document.getElementById("users-empty-search");
      const form = document.querySelector(".user-form");
      const preview = document.getElementById("score-preview");

      if (search) {
        search.addEventListener("input", () => {
          const query = search.value.trim().toLowerCase();
          let visibleCount = 0;

          cards.forEach((card) => {
            const text = card.dataset.search.toLowerCase();
            const visible = text.includes(query);
            card.classList.toggle("is-hidden", !visible);
            if (visible) visibleCount += 1;
          });

          if (empty) empty.classList.toggle("is-hidden", visibleCount !== 0);
        });
      }

      function metricValue(name) {
        const input = form?.elements[name];
        const value = Number.parseInt(input?.value || "0", 10);
        return Number.isFinite(value) && value > 0 ? value : 0;
      }

      function updateScorePreview() {
        if (!form || !preview) return;

        let score = 0;
        score += metricValue("events_created") * 4;
        score += metricValue("comments_count") * 2;
        score += metricValue("notes_count");
        score += metricValue("groups_joined") * 3;

        const dateValue = form.elements.active_date.value;
        if (dateValue && dateValue <= "{{today}}") score += 2;

        preview.textContent = score;
      }

      form?.addEventListener("input", updateScorePreview);
      form?.addEventListener("reset", () => setTimeout(updateScorePreview, 0));
      updateScorePreview();
    });
  </script>
</body>
</html>
