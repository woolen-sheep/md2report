FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app


FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python - 
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv



FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ sid main contrib non-free" > /etc/apt/sources.list &&\
       apt clean && apt update &&\
       apt-get -y install pandoc
COPY --from=poetry /app /app
EXPOSE 8000
CMD ["uvicorn","main:app","--workers","4"]
