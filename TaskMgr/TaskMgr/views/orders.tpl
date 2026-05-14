<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>TaskMgr - оформленные заказы</title>
  <link rel="stylesheet" href="/static/content/css/orders/orders.css" />
</head>
<body>
  <header class="orders-header">
    <div class="orders-container orders-header__inner">
      <a class="orders-logo" href="/">
        <span class="orders-logo__mark">T</span>
        <span>TaskMgr</span>
      </a>

      <nav class="orders-nav" aria-label="Основная навигация">
        <a href="/main">Расписание</a>
        <a class="active" href="/orders">Заказы</a>
        <a href="/active-users">Активные пользователи</a>
        <a href="/reg-auth">Вход</a>
      </nav>
    </div>
  </header>

  <main class="orders-container orders-page">
    <section class="orders-hero">
      <div>
        <p class="orders-eyebrow">Личный список</p>
        <h1>Оформленные заказы</h1>
        <p>
          Здесь показаны только заказы пользователя:
          {{current_user.get("display_name", current_user.get("username", ""))}}.
        </p>
      </div>
      <div class="orders-count">
        <strong>{{len(orders)}}</strong>
        <span>заказов</span>
      </div>
    </section>

    % if saved:
      <div class="page-notice page-notice--success">Заказ добавлен. Можно сразу внести следующий.</div>
    % end

    <section class="orders-layout">
      <form class="order-form" action="/orders" method="post" novalidate>
        <div class="section-title">
          <span>Новая запись</span>
          <h2>Добавить заказ</h2>
        </div>

        <label class="field">
          <span>Номер заказа</span>
          <input
            type="text"
            name="number"
            value="{{form.get('number', '')}}"
            placeholder="ORD-1004"
            autocomplete="off"
            required
          />
          % if errors.get("number"):
            <small class="field-error">{{errors["number"]}}</small>
          % end
        </label>

        <label class="field">
          <span>Автор / клиент</span>
          <input
            type="text"
            name="author"
            value="{{form.get('author', '')}}"
            placeholder="Имя или ник"
            required
          />
          % if errors.get("author"):
            <small class="field-error">{{errors["author"]}}</small>
          % end
        </label>

        <label class="field">
          <span>Описание</span>
          <textarea
            name="text"
            placeholder="Опишите состав и назначение заказа"
            required
          >{{form.get('text', '')}}</textarea>
          % if errors.get("text"):
            <small class="field-error">{{errors["text"]}}</small>
          % end
        </label>

        <div class="form-grid">
          <label class="field">
            <span>Дата</span>
            <input
              type="date"
              name="date"
              value="{{form.get('date', '')}}"
              max="{{today}}"
              required
            />
            % if errors.get("date"):
              <small class="field-error">{{errors["date"]}}</small>
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
            Проверьте поля формы. Данные не сброшены, исправьте ошибки и отправьте заказ еще раз.
          </div>
        % end

        <div class="form-actions">
          <button class="submit-button" type="submit">Разместить заказ</button>
          <button class="ghost-button" type="reset">Очистить</button>
        </div>
      </form>

      <section class="orders-list" aria-label="Список оформленных заказов">
        <div class="section-title">
          <span>Сортировка: свежие сверху</span>
          <h2>Перечень заказов</h2>
        </div>

        <div class="list-toolbar">
          <label class="search-field">
            <span>Поиск</span>
            <input type="search" id="orders-search" placeholder="Номер, автор, описание или телефон" />
          </label>
        </div>

        % if orders:
          <div class="order-cards" id="orders-list">
            % for order in orders:
              <article class="order-card" data-search="{{order['number']}} {{order['author']}} {{order['text']}} {{order['phone']}}">
                <div class="order-card__top">
                  <span class="order-number">{{order["number"]}}</span>
                  <time datetime="{{order['date']}}">{{order["date"]}}</time>
                </div>
                <h3>{{order["author"]}}</h3>
                <p>{{order["text"]}}</p>
                <a class="phone-link" href="tel:{{order['phone']}}">{{order["phone"]}}</a>
              </article>
            % end
          </div>
          <div class="empty-orders is-hidden" id="orders-empty-search">По такому запросу заказов не найдено.</div>
        % else:
          <div class="empty-orders">Заказов пока нет. Добавьте первый заказ через форму.</div>
        % end
      </section>
    </section>
  </main>

  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const search = document.getElementById("orders-search");
      const cards = Array.from(document.querySelectorAll(".order-card"));
      const empty = document.getElementById("orders-empty-search");

      if (!search) return;

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
    });
  </script>
</body>
</html>
