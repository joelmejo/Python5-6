mkdir CercaStringa
cp cerca.py CercaStringa
cp requirements.txt CercaStringa
pip install virtualenv
virtualenv myenv
source myenv/bin/activate
pip install -r requirements.txt
