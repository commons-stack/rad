FROM python:3.10.5
WORKDIR /app
COPY requirements.txt requirements.txt
COPY rad rad
RUN pip install -r requirements.txt
RUN pip install -e ./rad
CMD ["/bin/bash"]
