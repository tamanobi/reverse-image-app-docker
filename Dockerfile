FROM python:3.6.5-jessie

ARG project_dir=/web/
RUN pip install pipenv
WORKDIR $project_dir

ADD Pipfile.lock Pipfile $project_dir
RUN pipenv install -d

ADD gannoy.py app.py model.py $project_dir
RUN mkdir images
RUN pipenv run python -m model
CMD pipenv run python app.py
