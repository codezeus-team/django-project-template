test:
	sh bin/coverage.sh

# Generate a 32 character random string
# Found Here: http://www.howtogeek.com/howto/30184/10-ways-to-generate-a-random-password-from-the-command-line/
secret:
	@</dev/urandom tr -dc '12345!@#$%qwertQWERTasdfgASDFGzxcvbZXCVB' | head -c32; echo ""

init:
	pip install -r requirements/development.txt
	cp {{project_name}}/settings/local.example.py {{project_name}}/settings/local.py
	npm install -g gulp
	npm install
	chmod +x manage.py
	python manage.py makemigrations
	python manage.py migrate
	@echo
	@echo "Your new Django project is now set up!"
	@echo "To check the installation worked, first run the Django development server:"
	@echo
	@echo "    python manage.py runserver_plus"
	@echo
	@echo "Once that's running, you can start Gulp:"
	@echo
	@echo "    gulp"
	@echo
	@echo "A tab on your browser should open to 127.0.0.1:8001 with your new installation."
