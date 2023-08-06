# Audio Zen

## Usage 

### Build & Publish

```shell
# (Optional)
python -m pip install --user --upgrade setuptools wheel

python setup.py sdist bdist_wheel

python -m twine upload dist/*
```