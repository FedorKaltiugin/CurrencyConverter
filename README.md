This program allows you to convert the following currencies USD, CZK, EUR, PLN.

Start:
1. Fill in your data in the .env file

2. Build the project using the command:
docker-compose up --build

3. Create superuser using the command:
python manage.py createsuperuser

4. Set up Periodic tasks. The task will be converter.tasks.sample_task.
Start Datatime will be from today and now.

5. Go to the browser at 127.0.0.1:8000
