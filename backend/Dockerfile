FROM python:3.10-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y python3-venv && apt-get clean

RUN python -m venv /opt/task_tracker_venv

ENV PATH="/opt/task_tracker_venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]