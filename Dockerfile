FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY lambda_function.py techmeme_process_nlp.py file_processing.py  ${LAMBDA_TASK_ROOT}/

RUN python -m spacy download en_core_web_lg

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler"]