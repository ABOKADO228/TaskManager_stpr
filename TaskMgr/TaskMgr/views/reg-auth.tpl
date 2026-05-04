<!doctype html>
<html lang="ru">
<head>
  <link rel="stylesheet" type="text/css" href="/static/content/css/auth-reg/auth-reg.css" />
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>TaskMgr - вход</title>
</head>

<body>
  <main class="auth-shell">
    <section class="auth-brand">
      <a class="logo" href="/">
        <span class="logo__mark">T</span>
        <span>TaskMgr</span>
      </a>
      <div>
        <p class="eyebrow">Учебные группы и расписание</p>
        <h1>Один аккаунт для расписания, домашних заданий и событий группы</h1>
        <p class="lead">
          Создайте профиль, станьте старостой своей группы или присоединитесь как участник.
          Все данные прототипа сохраняются в браузере.
        </p>
      </div>
      <div class="feature-list">
        <span>Аккаунты</span>
        <span>Группы</span>
        <span>Роли</span>
        <span>Комментарии</span>
      </div>
    </section>

    <section class="auth-card" aria-label="Вход и регистрация">
      <div class="tabs">
        <button class="tab active" type="button" data-go="screen-login">Вход</button>
        <button class="tab" type="button" data-go="screen-register">Регистрация</button>
      </div>

      <form class="screen active" id="screen-login">
        <div class="header">Вход в аккаунт</div>

        <label class="field">
          <span>Логин</span>
          <input class="input" type="text" placeholder="Например, eduard" id="login-name" autocomplete="username" />
        </label>

        <label class="field">
          <span>Пароль</span>
          <input class="input" type="password" placeholder="Введите пароль" id="login-password" autocomplete="current-password" />
        </label>

        <label class="row">
          <input class="check" type="checkbox" id="remember" checked />
          <span>Запомнить вход</span>
        </label>

        <button class="btn" type="submit">Войти</button>
        <p class="message" id="login-message" aria-live="polite"></p>
      </form>

      <form class="screen" id="screen-register">
        <div class="header">Создать аккаунт</div>

        <label class="field">
          <span>Имя</span>
          <input class="input" type="text" placeholder="Ваше имя" id="register-display-name" autocomplete="name" />
        </label>

        <label class="field">
          <span>Логин</span>
          <input class="input" type="text" placeholder="Уникальный логин" id="register-name" autocomplete="username" />
        </label>

        <label class="field">
          <span>Пароль</span>
          <input class="input" type="password" placeholder="Минимум 4 символа" id="register-password" autocomplete="new-password" />
        </label>

        <button class="btn" type="submit">Зарегистрироваться</button>
        <p class="message" id="register-message" aria-live="polite"></p>
      </form>
    </section>
  </main>

  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const USERS_KEY = "taskmgr_users";
      const SESSION_KEY = "taskmgr_session";
      const redirectTarget = getRedirectTarget();

      const legacyUsers = [
        { id: "user-admin", username: "admin", displayName: "Администратор", password: "1234" },
        { id: "user-user1", username: "user1", displayName: "Пользователь", password: "1111" }
      ];

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

      // Возвращает безопасный адрес для перехода после входа.
      //
      // @returns
      // Внутренний путь сайта из параметра next или /main по умолчанию.
      //
      // @throws
      // Не выбрасывает исключения напрямую.
      //
      // @note
      // Проверка запрещает внешние URL, чтобы параметр next не стал открытым редиректом.
      function getRedirectTarget() {
        const next = new URLSearchParams(window.location.search).get("next");
        if (!next || !next.startsWith("/") || next.startsWith("//")) return "/main";
        return next;
      }

      // Сохраняет серверно-читаемые cookie текущего пользователя.
      //
      // @param user
      // Пользователь, который успешно вошел или зарегистрировался.
      //
      // @param remember
      // Флаг "Запомнить вход"; при true cookie живут 30 дней.
      //
      // @returns
      // Не возвращает значение.
      //
      // @throws
      // Не выбрасывает исключения напрямую.
      //
      // @note
      // Cookie нужны Bottle-маршруту /orders, потому что backend не может
      // прочитать localStorage браузера.
      function saveAuthCookies(user, remember) {
        const maxAge = remember ? "; max-age=2592000" : "";
        document.cookie = `taskmgr_user_id=${encodeURIComponent(user.id)}; path=/; SameSite=Lax${maxAge}`;
        document.cookie = `taskmgr_username=${encodeURIComponent(user.username)}; path=/; SameSite=Lax${maxAge}`;
        document.cookie = `taskmgr_display_name=${encodeURIComponent(user.displayName)}; path=/; SameSite=Lax${maxAge}`;
      }

      function ensureUsers() {
        const users = readJson(USERS_KEY, []);
        let changed = false;
        legacyUsers.forEach((seed) => {
          if (!users.some((user) => user.username === seed.username)) {
            users.push(seed);
            changed = true;
          }
        });
        if (changed) writeJson(USERS_KEY, users);
        return users;
      }

      function setMessage(id, text, type = "error") {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = text;
        el.dataset.type = type;
      }

      function createSession(user, remember) {
        const session = {
          userId: user.id,
          username: user.username,
          displayName: user.displayName,
          remember: Boolean(remember),
          startedAt: new Date().toISOString()
        };

        writeJson(SESSION_KEY, session);
        localStorage.setItem("isAuth", "true");
        localStorage.setItem("username", user.username);
        localStorage.setItem("userRole", "student");
        localStorage.setItem("rememberMe", remember ? "true" : "false");

        if (!remember) sessionStorage.setItem("tempAuth", "true");
        else sessionStorage.removeItem("tempAuth");

        saveAuthCookies(user, remember);
      }

      function normalizeLogin(value) {
        return value.trim().toLowerCase();
      }

      ensureUsers();

      const savedSession = readJson(SESSION_KEY, null);
      if (savedSession && localStorage.getItem("isAuth") === "true") {
        saveAuthCookies({
          id: savedSession.userId,
          username: savedSession.username,
          displayName: savedSession.displayName
        }, savedSession.remember);
        window.location.href = redirectTarget;
        return;
      }

      document.addEventListener("click", (event) => {
        const btn = event.target.closest("[data-go]");
        if (!btn) return;

        document.querySelectorAll(".screen").forEach((screen) => screen.classList.remove("active"));
        document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
        document.getElementById(btn.dataset.go)?.classList.add("active");
        btn.classList.add("active");
      });

      document.getElementById("screen-login").addEventListener("submit", (event) => {
        event.preventDefault();
        const users = ensureUsers();
        const username = normalizeLogin(document.getElementById("login-name").value);
        const password = document.getElementById("login-password").value;
        const remember = document.getElementById("remember").checked;

        if (!username || !password) {
          setMessage("login-message", "Введите логин и пароль.");
          return;
        }

        const user = users.find((item) => item.username === username);
        if (!user || user.password !== password) {
          setMessage("login-message", "Неверный логин или пароль.");
          return;
        }

        createSession(user, remember);
        window.location.href = redirectTarget;
      });

      document.getElementById("screen-register").addEventListener("submit", (event) => {
        event.preventDefault();
        const users = ensureUsers();
        const displayName = document.getElementById("register-display-name").value.trim();
        const username = normalizeLogin(document.getElementById("register-name").value);
        const password = document.getElementById("register-password").value;

        if (!displayName || !username || !password) {
          setMessage("register-message", "Заполните имя, логин и пароль.");
          return;
        }

        if (password.length < 4) {
          setMessage("register-message", "Пароль должен быть не короче 4 символов.");
          return;
        }

        if (users.some((user) => user.username === username)) {
          setMessage("register-message", "Такой логин уже занят.");
          return;
        }

        const user = {
          id: `user-${Date.now()}`,
          username,
          displayName,
          password
        };

        users.push(user);
        writeJson(USERS_KEY, users);
        createSession(user, true);
        window.location.href = redirectTarget;
      });
    });
  </script>
</body>
</html>
