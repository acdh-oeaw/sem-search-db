uv run coverage run manage.py test
uv run coverage html
cd htmlcov
uv run -m http.server 8080