<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>TaskMgr — управляй учёбой как профи</title>
  <link rel="stylesheet" href="/static/content/css/auth-reg/preview.css" />
</head>
<body>
  <div class="topbar">
    <div class="container topbar__inner">
      <span class="topbar__badge">Новый релиз</span>
      <span>Весенний семестр без авралов — подключай TaskMgr и держи дедлайны под контролем.</span>
    </div>
  </div>

  <header class="navbar">
    <div class="container navbar__inner">
      <a href="/" class="logo" aria-label="TaskMgr - главная">
        <span class="logo__mark">T</span>
        <span>TaskMgr</span>
      </a>

      <nav class="nav">
        <a href="#features">Возможности</a>
        <a href="#modes">Для кого</a>
        <a href="#platforms">Платформы</a>
        <a href="/orders">Заказы</a>
        <a href="/active-users">Активные пользователи</a>
        <a href="#news">Новинки</a>
      </nav>

      <div class="nav__actions">
        <span class="nav__status">Учебный прототип</span>
      </div>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero__banner">
          <div class="hero__content">
            <span class="eyebrow">TaskMgr для школьников и студентов</span>
            <h1>Учёба, проекты и дедлайны — в одном мощном центре управления</h1>
            <p>
              Планируй домашние задания, готовься к экзаменам, веди групповые проекты и отслеживай прогресс
              в интерфейсе с атмосферой большого digital-продукта.
            </p>

            <div class="hero__actions">
              <a class="btn btn--primary" href="/reg-auth">Начать работу</a>
            </div>

            <div class="hero__meta">
              <span>Домашние задания</span>
              <span>Расписание</span>
              <span>Командные проекты</span>
            </div>
          </div>

          <div class="slider-dots">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="features">
      <div class="container">
        <div class="section__head">
          <div>
            <h2>Рекомендуемые режимы работы</h2>
          </div>
          <span class="link-more">4 режима</span>
        </div>

        <div class="cards">
          <article class="card" style="background-image: url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80');">
            <div class="card__body">
              <span class="card__label">School Mode</span>
              <h3>Контроль домашних заданий</h3>
              <p>Разделяй предметы, следи за сроками сдачи и не теряй важные задания даже в загруженную неделю.</p>
              <div class="card__footer">
                <span>Предметы • сроки • приоритеты</span>
                <span>→</span>
              </div>
            </div>
          </article>

          <article class="card" style="background-image: url('https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=900&q=80');">
            <div class="card__body">
              <span class="card__label">Student Mode</span>
              <h3>Подготовка к сессии</h3>
              <p>Формируй чек-листы по экзаменам, разбивай подготовку на этапы и отслеживай прогресс по каждому курсу.</p>
              <div class="card__footer">
                <span>Экзамены • конспекты • дедлайны</span>
                <span>→</span>
              </div>
            </div>
          </article>

          <article class="card" style="background-image: url('https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=900&q=80');">
            <div class="card__body">
              <span class="card__label">Team Projects</span>
              <h3>Совместная работа</h3>
              <p>Назначай задачи в группе, распределяй роли и следи, кто отвечает за презентацию, код или исследование.</p>
              <div class="card__footer">
                <span>Команда • роли • статусы</span>
                <span>→</span>
              </div>
            </div>
          </article>

          <article class="card" style="background-image: url('https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=900&q=80');">
            <div class="card__body">
              <span class="card__label">Focus Mode</span>
              <h3>Личный план на день</h3>
              <p>Объединяй пары, занятия, повторение тем и личные задачи в одном динамическом расписании.</p>
              <div class="card__footer">
                <span>Фокус • привычки • день</span>
                <span>→</span>
              </div>
            </div>
          </article>
        </div>

        <div class="mini-grid" id="modes">
          <div class="panel">
            <div class="dashboard">
              <div class="dashboard__header">
                <div>
                  <h3>Сегодня в TaskMgr</h3>
                </div>
                <span class="tag tag--blue">4 задачи</span>
              </div>

              <div class="task">
                <div class="task__info">
                  <div class="task__check"></div>
                  <div>
                    <h4>Подготовить доклад по истории</h4>
                    <p>Срок: сегодня, 18:00 • 8 класс</p>
                  </div>
                </div>
                <span class="tag tag--green">Высокий</span>
              </div>

              <div class="task">
                <div class="task__info">
                  <div class="task__check"></div>
                  <div>
                    <h4>Собрать материалы для курсовой</h4>
                    <p>Срок: завтра • Университет</p>
                  </div>
                </div>
                <span class="tag tag--purple">Проект</span>
              </div>

              <div class="task">
                <div class="task__info">
                  <div class="task__check"></div>
                  <div>
                    <h4>Решить 10 задач по алгебре</h4>
                    <p>Срок: сегодня • Повторение перед контрольной</p>
                  </div>
                </div>
                <span class="tag tag--blue">Учёба</span>
              </div>
            </div>
          </div>

          <div class="panel platforms" id="platforms">
            <h3>Где доступен сервис</h3>
            <p style="color: var(--muted); margin-top: 6px;">TaskMgr одинаково удобно использовать дома, в школе, в вузе и на ходу.</p>

            <div class="platforms__list">
              <div class="platform">
                <div class="platform__left">
                  <div class="platform__icon">W</div>
                  <div>
                    <strong>Web App</strong><br />
                    <small>Полный доступ через браузер</small>
                  </div>
                </div>
                <span class="tag tag--blue">Online</span>
              </div>

              <div class="platform">
                <div class="platform__left">
                  <div class="platform__icon">M</div>
                  <div>
                    <strong>Mobile</strong><br />
                    <small>Быстрый просмотр дедлайнов</small>
                  </div>
                </div>
                <span class="tag tag--green">Soon</span>
              </div>

              <div class="platform">
                <div class="platform__left">
                  <div class="platform__icon">T</div>
                  <div>
                    <strong>Team Access</strong><br />
                    <small>Для групповых проектов и классов</small>
                  </div>
                </div>
                <span class="tag tag--purple">Beta</span>
              </div>
            </div>
          </div>
        </div>

        <div class="cta" id="news">
          <div>
            <h2>Готов начать новый учебный сезон сильнее?</h2>
            <p>Создай аккаунт, перенеси предметы и дедлайны в систему, а потом управляй ими из красивого, насыщенного интерфейса в стиле крупного продуктового портала.</p>
          </div>
          <span class="tag tag--blue">Регистрация доступна</span>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container footer__inner">
      <div>© 2026 TaskMgr. Учись без хаоса.</div>
      <div>О сервисе • Поддержка • Политика конфиденциальности</div>
    </div>
  </footer>
</body>
</html>
