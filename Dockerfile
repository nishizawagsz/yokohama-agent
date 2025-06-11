FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Portot nyitunk és háttérben elindítjuk a scraper-t, majd egy minimális HTTP szervert.
CMD ["sh", "-c", "python main.py & python -m http.server 10000"]
