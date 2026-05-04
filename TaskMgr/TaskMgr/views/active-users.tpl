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
        <a href="/">Главная</a>
        <a href="/reg-auth">Вход</a>
        <a href="/main">Расписание</a>
        <a href="/orders">Заказы</a>
        <a class="active" href="/active-users">Активные пользователи</a>
      </nav>
    </div>
  </header>

  <main class="users-container users-page">
    <section class="users-hero">
      <div>
        <p class="users-eyebrow">Вариант 6</p>
        <h1>Активные пользователи</h1>
        <p>
          Список загружается Python-кодом из файла. Нового активного пользователя
          можно добавить через форму с серверной проверкой даты и телефона.
        </p>
      </div>
      <div class="users-count">
        <strong>{{len(users)}}</strong>
        <span>пользователей</span>
      </div>
    </section>

    <section class="users-layout">
      <form class="user-form" action="/active-users" method="post" novalidate>
        <div class="section-title">
          <span>Новый объект данных</span>
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

        % if errors:
          <div class="form-alert">
            Проверьте введенные данные. Значения сохранены, исправьте ошибки и повторите отправку.
          </div>
        % end

        <button class="submit-button" type="submit">Добавить пользователя</button>
      </form>

      <section class="users-list" aria-label="Список активных пользователей">
        <div class="section-title">
          <span>Сортировка: самые активные по дате сверху</span>
          <h2>Перечень пользователей</h2>
        </div>

        % if users:
          <div class="user-cards">
            % for user in users:
              <article class="user-card">
                <div class="user-card__top">
                  <span class="user-nick">@{{user["nick"]}}</span>
                  <time datetime="{{user['active_date']}}">{{user["active_date"]}}</time>
                </div>
                <p>{{user["description"]}}</p>
                <a class="phone-link" href="tel:{{user['phone']}}">{{user["phone"]}}</a>
              </article>
            % end
          </div>
        % else:
          <div class="empty-users">Активных пользователей пока нет. Добавьте первого участника через форму.</div>
        % end
      </section>
    </section>
  </main>
</body>
</html>
