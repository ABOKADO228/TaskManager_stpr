<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Week Calendar</title>

    <link rel="stylesheet" href="/static/content/css/tokens.css" />
    <link rel="stylesheet" href="/static/content/css/main/main.css" />
  </head>

  <body>
    <div class="window" id="week-calendar-window">
      <div class="content" id="content">

        <div class="left-panel" id="left-panel">
          <div class="name-block" id="LabelName"></div>

          <div class="data-actions" id="data-actions">
            <button type="button" class="menu-btn" id="DownloadData">Загрузить данные</button>
            <button type="button" class="menu-btn" id="UploadData">Выгрузить данные</button>
          </div>

          <div class="notes-title" id="notes-title">Заметки</div>
          <div class="notes-box" id="notes-box">
            <textarea id="notes-text" rows="10" cols="30"></textarea>
          </div>
        </div>

        <div class="panel calendar-panel" id="calendar-panel">
          <div class="panel-header">Расписание</div>

          <div class="calendar-body" id="calendar-body">
            <div class="nd-label" id="numerator-label">Числитель</div>
            <div class="days-grid" id="numerator-days"></div>

            <div class="week-nav">
              <button type="button" class="nav-btn" id="PreviousWeek">◄</button>
              <div class="month-year" id="MonthYearText"></div>
              <button type="button" class="nav-btn" id="NextWeek">►</button>
            </div>

            <div class="nd-label" id="denominator-label">Знаменатель</div>
            <div class="days-grid" id="denominator-days"></div>
          </div>
        </div>

        <div class="panel info-panel" id="info-panel">
          <div class="panel-header">Информация</div>

          <div class="info-body" id="info-body">
            <span class="placeholder" id="placeHolderText">
              Выберите предмет для отображения информации
            </span>

            <div id="ucInformation" style="display:none;"></div>
          </div>
        </div>

      </div>
      <div id="Settings" style="display:none;"></div>
    </div>

    <script src="/static/scripts/week-calendar.js"></script>
  </body>
</html>