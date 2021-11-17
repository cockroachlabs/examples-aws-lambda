FROM public.ecr.aws/lambda/python:3.8

COPY init_db.py ${LAMBDA_TASK_ROOT}
COPY certs ./certs
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "init_db.lambda_handler" ]