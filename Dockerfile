FROM python:3.9


ADD Home.py .
COPY . .

RUN pip install streamlit plotly

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "Home.py"]