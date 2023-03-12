# test
Для запуска проекта используем команду (для всех комманд лучше использовать sudo) "docker compose build"? 

Далее выполняем эти команды
"sudo docker compose run python3 manage.py makemigrations"
"sudo docker compose run web python3 manage.py migrate"


после чего поднимаем сам контейнер "docker compose up".
