FROM ubuntu:latest

RUN apt update \
    && apt install -y python3 python3-pip\
    && pip install --upgrade pip

COPY dist/StudentDiary-0.0.0-py3-none-any.whl ./
RUN pip install StudentDiary-0.0.0-py3-none-any.whl
ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install -y python3-tk

CMD [ "python3", "-m", "diary" ]