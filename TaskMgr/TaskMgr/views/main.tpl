<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <title>Week Calendar</title>
  <link rel="stylesheet" href="/static/content/css/main/main.css" />
</head>

<body>
<div class="window">
  <div class="content">

    <!-- LEFT -->
    <div class="left-panel">
      <div class="name-block">Eduard Tigranyan</div>

      <div class="data-actions">
        <button class="data-action-button">Настройки</button>
      </div>

      <div class="notes-title">Заметки</div>

      <div class="notes-box">
        <textarea></textarea>
      </div>
    </div>

    <!-- CENTER -->
    <div class="panel">
      <div class="panel-header">Расписание</div>

      <div class="calendar-body">
        <div class="nd-label">Числитель</div>
        <div class="days-grid" id="numerator-days"></div>

        <div class="week-nav">
          <button class="nav-btn">◄</button>
          <div class="month-year" id="MonthYearText"></div>
          <button class="nav-btn">►</button>
        </div>

        <div class="nd-label">Знаменатель</div>
        <div class="days-grid" id="denominator-days"></div>
      </div>
    </div>

    <!-- RIGHT -->
    <div class="panel info-panel">
      <div class="panel-header">Информация</div>
      <div class="info-body">
        <span class="placeholder">
          Выберите предмет для отображения информации
        </span>
      </div>
    </div>

  </div>
</div>

<script src="/static/scripts/week-calendar.js"></script>
</body>
</html>