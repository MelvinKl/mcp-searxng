FROM python:3.13

WORKDIR /app
RUN pip install uv

COPY . .
RUN uv sync --no-dev

CMD [ "uv", "run", "python", "src/main.py"]