FROM python:3.10-slim AS builder

WORKDIR /app-setup

ADD https://install.python-poetry.org ./install-poetry.py
RUN python ./install-poetry.py && rm ./install-poetry.py

COPY ./pyproject.toml ./poetry.lock ./
RUN /root/.local/bin/poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install -r requirements.txt --target=/python \
    && rm requirements.txt


FROM python:3.10-slim

WORKDIR /app

RUN pip install gunicorn

COPY --from=builder /python /python
COPY ./supreme_umbrella ./supreme_umbrella

RUN groupadd -g 1000 app && useradd -M -u 1000 -g app app
USER app

ENV PYTHONPATH=/python
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0", "-w", "4", "supreme_umbrella.main:app"]
