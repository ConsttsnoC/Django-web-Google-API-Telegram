
<!-- Заголовок -->
<h1 align="center">
  <br>
   Django-приложение с использованием Google API + получение курса ЦБ + Telegram
  <br>
</h1>
<!-- Описание -->
<p align="center">
  <a href="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" target="_blank">

  </a>
</p>
<!-- Иконки -->
<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10.7-green">
    <img src="https://img.shields.io/badge/Django-4.1.6-yellow">
    <img src="https://img.shields.io/badge/Telegram-13.8-blue">
    <img src="https://img.shields.io/badge/Postgresql-15.2-orange">
    <img src="https://img.shields.io/badge/Deploy-Docker-blueviolet">
    <img src="https://img.shields.io/badge/Google API-red">
</p>

 <div>
      <h1>Всем привет, я <a href="https://www.gilmanov.net/" target="_blank">Константин</a> <img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
      <h3>Этот репозиторий содержит решение тестового задания по созданию Python-приложения:
        <li>Создано на Django</li>
        <li>База данных Postgresql</li>
        <li>Одностраничное веб-приложение</li>
        <li>Telegram-bot с оповещением</li>
        <li>Использование Google API</li>
        <li>Форматирование кода с помощью autopep8</li></h3>


<h3><img src="https://img.icons8.com/dusk/64/000000/rocket.png" height="30"/> Инструкция по работе с приложением <img src="https://img.icons8.com/dusk/64/000000/rocket.png" height="30"/></h3>
<ul>
    <li>У вас должен быть установлен Postgresql</li>
    <li>Переходим в Postgresql создаем таблицу c названием <code>my_table</code>:
<p>CREATE TABLE IF NOT EXISTS public.my_table</p>
(
    name integer,
    order_number integer,
    price numeric(10,2),
    date date,
    price_rub numeric(10,2)
)

<p>TABLESPACE pg_default;</p>

<p>ALTER TABLE IF EXISTS public.my_table</p>
    <p>OWNER to postgres;</p>
	 </li>
    <li>Переходим в файл  <code>.env.dev</code> и заменяем на ваши данные из Postgresql</li>
    <li>Переходим в файл <code>__main__.py</code> и заменяем на ваши данные из Postgresql в функции <code>get_database_connection()</code></li>
    <li>Переходим в файл  <code>docker-compose.yml</code> и заменяем на ваши данные из Postgresql</li>
    <li>Переходим в <code>Dockerfile</code> и запускаем его</li>
</ul>

<h3><img src="https://img.icons8.com/dusk/64/000000/campfire.png" height="30"/> Идем дальше? Тогда запускаем Docker<img src="https://img.icons8.com/dusk/64/000000/campfire.png" height="30"/></h3>

<h3><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" height="30"/> Docker</h3>
<p>Чтобы запустить приложение через Docker, выполните следующие шаги:</p>
<ol>
<li>Загрузите и установите <a href="https://www.docker.com/products/docker-desktop/">Docker</a></li>
<li>Перейти в папку с приложением<code>cd \app_root></code></li>
<li>Собрать проект <code>docker-compose build</code></li>
<li>Запустить проект <code>docker-compose up</code></li>
</ol>

<h3><img src="https://img.icons8.com/dusk/64/000000/rocket.png" height="30"/> Инструкция по работе с приложением <img src="https://img.icons8.com/dusk/64/000000/rocket.png" height="30"/></h3>
<ul>
    <li>Переходим в файл <code>__main__.py</code> и запускаем (RUN) его</li>
    <li>Заходим к себе в приложение <code>telegram</code> и находим в поиске <code>@userinfobot</code> и берем оттуда свой id-чата
    <li>Переходим в папку <code>telegram</code> и открываем там файл <code>alert_kanal_bot.py</code> и вставляем в переменную <code>chat_id</code> и в обработчик-команд <code>send_order_message_at_time</code> ваш id-чата</li>
    <li>В файле <code>alert_kanal_bot.py</code> меняем в ДВУХ переменных <code>conn</code> данные на ваши данные из Postgresql</li>
    <li>Запускаем (RUN)  файл <code>alert_kanal_bot.py</code></li>
</ul>
