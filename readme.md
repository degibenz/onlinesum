web-приложение, которое:

- Позволяет выбрать произвольное целое число в интервале от 1 до 10.
- Отображает в режиме реального времени сумму чисел, выбранных всеми пользователями, находящимися сейчас в приложении.
- Легко масштабируется на большое количество пользователей.

#API

##Client/Session
* POST /session - метод создает новую сессию на сервер и возвращает токен

##Vote
* POST /vote - метод указывает, что пользователь выбрал число

Чтобы проголосовать в заголовке запроса надо передать x-token и соот полученный токен
``` python  
  {
    'number' : <int>
  }
```

##Online
* WS /online - веб-сокет, сюда приходят данные об обновившейся сумме всех выбранных числах