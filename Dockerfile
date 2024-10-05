FROM alpine

COPY . /app

ENTRYPOINT [ "sleep" ]
CMD [ "3600" ]