<!doctype html>
<html lang="ru">
<head>
  <link rel="stylesheet" type="text/css" href="/static/content/css/auth-reg/auth-reg.css" />
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Start</title>
</head>

<body>
  <div class="window" role="application" aria-label="Start">
    <div class="content">

      <section class="screen active" id="screen-login">
        <div class="header">Вход в аккаунт</div>

        <div class="field">
          <input class="input" type="text" placeholder="Имя" id="name-field"/>
        </div>

        <div class="field">
          <input class="input" type="password" placeholder="Пароль" id="password-field"/>
        </div>

        <div class="row">
          <input class="check" type="checkbox" id="remember" />
          <span>Запомнить вход</span>
        </div>

        <button class="btn" type="button" id="enter-button">Войти</button>

        <div class="bottom">
          <div class="bottom-grid">
            <div class="muted">Нет аккаунта?</div>
            <button class="text-btn red" type="button" data-go="screen-register">Регистрация</button>
          </div>
        </div>
      </section>

      <section class="screen" id="screen-register">
        <div class="header">Регистрация</div>

        <div class="field">
          <input class="input" type="text" placeholder="Имя" />
        </div>

        <div class="field">
          <input class="input" type="password" placeholder="Пароль" />
        </div>

        <button class="btn" type="button">Зарегистрировать</button>

        <div class="bottom">
          <div class="bottom-grid">
            <div class="muted">Уже есть аккаунт?</div>
            <button class="text-btn" type="button" data-go="screen-login">Войти</button>
          </div>
        </div>
      </section>

    </div>
  </div>

  <script>
    document.addEventListener("DOMContentLoaded", () => {

      const users = {
        admin: { password: "1234", role: "admin" },
        user1:  { password: "1111", role: "user"  }
      };

      const inputName = document.getElementById("name-field");
      const inputPass = document.getElementById("password-field");
      const rememberToggle = document.getElementById("remember");
      const enterBtn = document.getElementById("enter-button");

      console.log("auth script loaded", { inputName: !!inputName, inputPass: !!inputPass, rememberToggle: !!rememberToggle, enterBtn: !!enterBtn });

      function show(id) {
        document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
        const el = document.getElementById(id);
        if (el) el.classList.add("active");
      }

      document.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-go]");
        if (!btn) return;
        show(btn.dataset.go);
      });

      function saveAuth({ username, role }, remember) {
        localStorage.setItem("isAuth", "true");
        localStorage.setItem("username", username);
        localStorage.setItem("userRole", role);
        localStorage.setItem("rememberMe", remember ? "true" : "false");

        if (!remember) sessionStorage.setItem("tempAuth", "true");
        else sessionStorage.removeItem("tempAuth");
      }

      function clearAuth() {
        localStorage.removeItem("isAuth");
        localStorage.removeItem("username");
        localStorage.removeItem("userRole");
        localStorage.removeItem("rememberMe");
        sessionStorage.removeItem("tempAuth");
      }

      function isAuthed() {
        return localStorage.getItem("isAuth") === "true";
      }

      (function init() {
        const remember = localStorage.getItem("rememberMe");
        const tempMarker = sessionStorage.getItem("tempAuth");

        if (remember === "false" && !tempMarker) {
          clearAuth();
        }

        if (rememberToggle) rememberToggle.checked = (localStorage.getItem("rememberMe") === "true");

        const savedUsername = localStorage.getItem("username");
        if (savedUsername && inputName) inputName.value = savedUsername;

        if (isAuthed()) {
          console.log("already authed -> /main");
          window.location.href = "/main";
        }
      })();

      if (!enterBtn) return;

      enterBtn.addEventListener("click", () => {
        console.log("click login");

        const username = (inputName?.value ?? "").trim();
        const password = inputPass?.value ?? "";
        const remember = rememberToggle ? rememberToggle.checked : true;

        if (!username || !password) return alert("Введите логин и пароль");

        const user = users[username];
        if (!user || user.password !== password) return alert("Неверный логин или пароль");

        saveAuth({ username, role: user.role }, remember);

        console.log("redirect -> /main", {
          isAuth: localStorage.getItem("isAuth"),
          username: localStorage.getItem("username"),
          rememberMe: localStorage.getItem("rememberMe"),
        });

        window.location.href = "/main";
      });

    });
  </script>
</body>
</html>