<!doctype html>
<html lang="ru">

<!doctype html>
<html lang="ru">
<head>
    <link rel="stylesheet" href="css/tokens.css">
    <link rel="stylesheet" href="/static/content/AuthReg/Auth.css" />
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
          <input class="input" type="text" placeholder="Имя" />
        </div>

        <div class="field">
          <input class="input" type="password" placeholder="Пароль" />
        </div>

        <div class="row">
          <input class="check" type="checkbox" id="remember" />
          <span>Запомнить вход</span>
        </div>

        <button class="btn" type="button">Войти</button>

        <div class="bottom">
          <div class="bottom-grid">
            <div class="muted">Нет аккаунта?</div>
            <button class="text-btn red" type="button" data-go="screen-register">Регистрация</button>
          </div>
        </div>
      </section>

      <section class="screen" id="screen-register">
        <div class="header" style="background: rgba(43,134,255,.10); border-color: rgba(255,255,255,.12);">
          Регистрация
        </div>

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
    function show(id){
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
      const el = document.getElementById(id);
      if (el) el.classList.add('active');
    }

    document.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-go]');
      if (!btn) return;
      show(btn.dataset.go);
    });
  </script>
</body>
</html>