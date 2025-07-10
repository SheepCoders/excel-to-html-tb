## Installing / Getting started

Python3 and Git must be already installed

```shell
git clone https://github.com/SheepCoders/excel-to-html-tb.git
cd excel-to-html-tb
python3 -m venv venv
for linux : "source venv/bin/activate"; for windows "venv\Scripts\activate"
pip install -r requirements.txt
python manage.py runserver
```


user: test
email: test@test.com
pwd: testpass


Note for developer:
-find convenient place for: activity.roun_up_to, MULTIPLICITIES_ROUN_UP_TO, RES_ROUND_UP_TO
-check left hand down calcul-s
-translate to polish
-del review data from db
- in calculations.py in def cai() maybee should be activity.hand ( not "right"). In cti() the same...
- BB11-16 (Q1 -Q3 how works?)
- H17 H42 for indicator ( not activity)