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
          <input class="input" type="password" placeholder="Минимум 8 символов" id="register-password" autocomplete="new-password" />
        </label>

        <label class="field">
          <span>Повтор пароля</span>
          <input class="input" type="password" placeholder="Повторите пароль" id="register-password-repeat" autocomplete="new-password" />
        </label>

        <button class="btn" type="submit">Зарегистрироваться</button>
        <p class="message" id="register-message" aria-live="polite"></p>
      </form>
    </section>
  </main>

  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const SESSION_KEY = "taskmgr_session";
      const redirectTarget = getRedirectTarget();

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

      function getRedirectTarget() {
        const next = new URLSearchParams(window.location.search).get("next");
        if (!next || !next.startsWith("/") || next.startsWith("//")) return "/main";
        return next;
      }

      function saveAuthCookies(user, remember) {
        const maxAge = remember ? "; max-age=2592000" : "";
        document.cookie = `taskmgr_user_id=${encodeURIComponent(user.id)}; path=/; SameSite=Lax${maxAge}`;
        document.cookie = `taskmgr_username=${encodeURIComponent(user.username)}; path=/; SameSite=Lax${maxAge}`;
        document.cookie = `taskmgr_display_name=${encodeURIComponent(user.displayName)}; path=/; SameSite=Lax${maxAge}`;
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

      function setMessage(id, text, type = "error") {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = text;
        el.dataset.type = type;
      }

      function clearMessage(id) {
        setMessage(id, "");
      }

      function setFormBusy(formId, busy) {
        const form = document.getElementById(formId);
        if (!form) return;
        form.querySelectorAll("button, input").forEach((element) => {
          if (element.type === "checkbox") return;
          element.disabled = busy;
        });
      }

      async function postJson(url, body) {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(body)
        });

        let data = {};
        try {
          data = await response.json();
        } catch {
          data = {};
        }

        if (!response.ok) {
          const message = data.message || Object.values(data.errors || {})[0] || "Не удалось выполнить запрос.";
          throw new Error(message);
        }

        return data;
      }

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
        clearMessage("login-message");
        clearMessage("register-message");
      });

      document.getElementById("screen-login").addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("login-message");

        const username = (document.getElementById("login-name").value || "").trim().toLowerCase();
        const password = document.getElementById("login-password").value || "";
        const remember = document.getElementById("remember").checked;

        if (!username || !password) {
          setMessage("login-message", "Введите логин и пароль.");
          return;
        }

        setFormBusy("screen-login", true);
        try {
          const data = await postJson("/api/auth/login", { username, password });
          createSession(data.user, remember);
          window.location.href = redirectTarget;
        } catch (error) {
          setMessage("login-message", error.message || "Неверный логин или пароль.");
        } finally {
          setFormBusy("screen-login", false);
        }
      });

      document.getElementById("screen-register").addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("register-message");

        const displayName = document.getElementById("register-display-name").value.trim();
        const username = (document.getElementById("register-name").value || "").trim().toLowerCase();
        const password = document.getElementById("register-password").value || "";
        const passwordRepeat = document.getElementById("register-password-repeat").value || "";

        if (!displayName || !username || !password || !passwordRepeat) {
          setMessage("register-message", "Заполните имя, логин, пароль и повтор пароля.");
          return;
        }

        if (password.length < 8) {
          setMessage("register-message", "Пароль должен быть не короче 8 символов.");
          return;
        }

        if (password !== passwordRepeat) {
          setMessage("register-message", "Пароли не совпадают.");
          return;
        }

        setFormBusy("screen-register", true);
        try {
          const data = await postJson("/api/auth/register", {
            display_name: displayName,
            username,
            password,
            password_repeat: passwordRepeat
          });
          createSession(data.user, true);
          window.location.href = redirectTarget;
        } catch (error) {
          setMessage("register-message", error.message || "Не удалось зарегистрировать пользователя.");
        } finally {
          setFormBusy("screen-register", false);
        }
      });
    });
  </script>
</body>
</html>
