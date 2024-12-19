# php-test-task

# # Pre requirements:
- Go to the **web** directory
- Create .env file in **web** directory and fill it by .env.example file (because it contains all required variables for laravel project)
- Add strong passwords to both fields: **DB_PASSWORD** and **DB_ROOT_PASSWORD**
- Run `composer install --no-dev --optimize-autoloader` in **web** directory
- Run `php artisan key:generate` in **web** directory
- Return to the root directory of the project

# # How to build:
- Run `docker-compose --env-file ./web/.env up --build`

# # How to run parsing algorythm:
- Run `docker exec -it parser xvfb-run -a python3 /parser/main.py`