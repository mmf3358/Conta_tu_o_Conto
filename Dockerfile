FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8501 DEVICE=cpu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY project ./project
COPY app.py .
COPY .streamlit ./.streamlit
EXPOSE 8501
CMD ["sh", "-c", "python -m streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8501} --server.headless=true"]
