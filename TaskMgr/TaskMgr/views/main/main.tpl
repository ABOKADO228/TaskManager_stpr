<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Week Calendar</title>
    <link rel="stylesheet" href="/static/main/main.css" />
  </head>

  <body>
    <div class="window" id="week-calendar-window">
      <div class="content" id="content">
        <!-- LEFT: Grid menu -->
        <div class="left-panel" id="left-panel">
          <div class="name-block" id="LabelName">
            <!-- сюда имя пользователя -->
          </div>

          <div class="data-actions" id="data-actions">
            <button type="button" class="menu-btn" id="DownloadData">Загрузить данные</button>
            <button type="button" class="menu-btn" id="UploadData">Выгрузить данные</button>
          </div>

          <div class="notes-title" id="notes-title">Заметки</div>

          <div class="notes-box" id="notes-box">
            <textarea id="notes-text" rows="10" cols="30"></textarea>
          </div>
        </div>

        <!-- CENTER: Grid calendar -->
        <div class="panel calendar-panel" id="calendar-panel">
          <div class="panel-header">Расписание</div>

          <div class="calendar-body" id="calendar-body">
            <div class="nd-label" id="numerator-label">Числитель</div>

            <!-- Numerator days -->
            <div class="days-grid" id="numerator-days">
              <div class="day-card">День 1</div>
              <div class="day-card">День 2</div>
              <div class="day-card">День 3</div>
              <div class="day-card">День 4</div>
              <div class="day-card">День 5</div>
              <div class="day-card">День 6</div>
              <div class="day-card">День 7</div>
            </div>

            <!-- Week navigation (between blocks) -->
            <div class="week-nav" id="week-nav">
              <button type="button" class="nav-btn" id="PreviousWeek">◄</button>
              <div class="month-year" id="MonthYearText"></div>
              <button type="button" class="nav-btn" id="NextWeek">►</button>
            </div>

            <div class="nd-label" id="denominator-label">Знаменатель</div>

            <!-- Denominator days -->
            <div class="days-grid" id="denominator-days">
              <div class="day-card">День 1</div>
              <div class="day-card">День 2</div>
              <div class="day-card">День 3</div>
              <div class="day-card">День 4</div>
              <div class="day-card">День 5</div>
              <div class="day-card">День 6</div>
              <div class="day-card">День 7</div>
            </div>
          </div>
        </div>

        <!-- RIGHT: Grid Information -->
        <div class="panel info-panel" id="info-panel">
          <div class="panel-header">Информация</div>

          <div class="info-body" id="info-body">
            <span class="placeholder" id="placeHolderText">
              Выберите предмет для отображения информации
            </span>

            <!-- аналог UserControls:ucInformation -->
            <div id="ucInformation" style="display:none;"></div>
          </div>
        </div>
      </div>

      <!-- Settings (как в XAML, скрыто) -->
      <div id="Settings" style="display:none;"></div>
    </div>
    <button id="logout-button">LOGOUT </button>
  </body>
  
  <script>
    document.addEventListener("DOMContentLoaded", () => {
        if (localStorage.getItem("isAuth") !== "true") {
            window.location.replace("/");
            return;
        };

        document.getElementById("logout-button").addEventListener('click', () => {
            localStorage.removeItem("isAuth");
            localStorage.removeItem("username");
            localStorage.removeItem("userRole");
            localStorage.removeItem("rememberMe");
            sessionStorage.removeItem("tempAuth");
            window.location.replace("/");
        });

        window.addEventListener("storage", (event) => {
            if (event.key === "isAuth" && event.newValue !== "true") {
              window.location.replace("/");
              }
            });
    });
  
  </script>
</html>