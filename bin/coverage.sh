py.test --cov-config .coveragerc \
        --cov-report html \
        --cov {{project_name}}/apps && \
python -c "import webbrowser, os; \
           webbrowser.open('file://' + os.getcwd() + \
                           '/htmlcov/index.html')"
