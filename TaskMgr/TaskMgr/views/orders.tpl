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
        <a class="active" href="/orders">Оформленные заказы</a>
        <a href="/active-users">Активные пользователи</a>
        <a href="/reg-auth">Вход</a>
      </nav>
    </div>
  </header>

  <main class="orders-container orders-page">
    <section class="orders-hero">
      <div>
        <p class="orders-eyebrow">Практическая интеграция Bottle</p>
        <h1>Оформленные заказы</h1>
        <p>
          Список загружается Python-кодом из JSON-файла. На странице видны только заказы
          текущего пользователя: {{current_user.get("display_name", current_user.get("username", ""))}}.
        </p>
      </div>
      <div class="orders-count">
        <strong>{{len(orders)}}</strong>
        <span>ваших заказов</span>
      </div>
    </section>

    <section class="orders-layout">
      <form class="order-form" action="/orders" method="post" novalidate>
        <div class="section-title">
          <span>Новый объект данных</span>
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
            Проверьте поля формы. Данные не сброшены, исправьте ошибки и отправьте заказ ещё раз.
          </div>
        % end

        <button class="submit-button" type="submit">Разместить заказ</button>
      </form>

      <section class="orders-list" aria-label="Список оформленных заказов">
        <div class="section-title">
          <span>Сортировка: свежие сверху</span>
          <h2>Перечень заказов</h2>
        </div>

        % if orders:
          <div class="order-cards">
            % for order in orders:
              <article class="order-card">
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
        % else:
          <div class="empty-orders">Заказов пока нет. Добавьте первый объект через форму.</div>
        % end
      </section>
    </section>
  </main>
</body>
</html>
