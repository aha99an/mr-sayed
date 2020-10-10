import os
from django.core.wsgi import get_wsgi_application
import xlrd
import uuid
from googletrans import Translator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr-syed.settings')
application = get_wsgi_application()
from questions.models import MrQuestion
from classes.models import Class
from accounts.models import CustomUser, Counter
from googletrans import Translator
translator = Translator()

# CustomUser.objects.filter(id__gte=10).delete()
xl_workbook = xlrd.open_workbook("students-sheet.xlsx")
classes = Class.objects.all()

counter = Counter.objects.all().last()
k=counter.counter
xl_sheet = xl_workbook.sheet_by_index(k)
sheet = []
for row in range(xl_sheet.nrows):
    sheet.append([xl_sheet.cell(row, col).value for col in range(xl_sheet.ncols)])

for i in range(1, len(sheet)):
    english_name = translator.translate(sheet[i][0]).text
    english_name = english_name.replace(" ", "_")
    email = english_name + "_" + str(k)+str(i) + "@mrsyed.com"
    CustomUser.objects.create_user(username=email, first_name=sheet[i][0],
                                    student_is_active=True, school=sheet[i][2], student_class=classes.get(name=sheet[i][1])).reset_password()
counter.counter = k+1
counter.save()