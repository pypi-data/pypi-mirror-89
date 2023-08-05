FROM hub.sky-cloud.net/cicd/nmap-python:latest
MAINTAINER fangcong
COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
WORKDIR /project/
ENV PATH=$PATH:/project
ENV PYTHONPATH /project
CMD ["python3","/src/nmap-driver.py"]
