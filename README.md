# PIR – ML Model Training

##1:

windows: `pip install --upgrade pyenv-win`

linux: `pip install --upgrade pyenv`

---

##2:

`pip install --upgrade pipenv`

---

##3:

windows: `pyenv install 3.7.9 && pipenv --python %USERPROFILE%\.pyenv\pyenv-win\versions\3.7.9\python.exe install --dev`

linux: `pipenv install --dev`

---

##4:

`pipenv run prepare && pipenv run split && pipenv run train && pipenv run generate`

---

##5:

Final model file: `output/model.cc`