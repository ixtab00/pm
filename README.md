# Password Manager

**Password Manager** — веб-приложение на **Flask** для хранения паролей. Пароли зашифрованы с помощью AES.
Аутентификация осуществляется через OTP (письмо с одноразовым кодом на email). Пользователь может узнать, не был ли его
пароль в утечках данных прямо в приложении.
---

## Возможности
- Регистрация и вход с OTP-подтверждением (регистрация происходит при первом входе)
- Шифрование паролей через AES
- Проверка паролей по Have I Been Pwned API
- Управление сохранёнными паролями (CRUD)

## Технологии
- **Backend:** Flask, SQLAlchemy  
- **Security:** AES, OTP, smtplib, HIBP API  
- **Database:** SQLite + SQLAlchemy

## Установка и запуск
```bash
git clone https://github.com/ixtab00/pm
cd pm
pip install -r requirements.txt
flask run
```
