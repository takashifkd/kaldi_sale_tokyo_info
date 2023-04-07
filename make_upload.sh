rm upload.zip
rm -r upload/
rm -r download/

mkdir -p download/bin
mkdir upload

cp -r download/bin upload/bin
cp app/lambda_function.py upload/

pip install -r app/requirements.txt -t upload/
cd upload/
zip -r ../upload.zip --exclude=__pycache__/* .

rm -r upload/
rm -r download/
