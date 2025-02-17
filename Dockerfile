FROM python:3.10.16
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python api.py & streamlit run app.py