import csv
from django.db import models
from django.conf import settings

class State(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return 'State: %s' % self.code

state_data_attrs = {
    'state': models.ForeignKey(State),
    'year': models.PositiveSmallIntegerField()
}

STATE_DATE_COLUMN_NAMES = {}
for row in csv.reader(open(settings.STATE_DATA_COLUMNS_FILE, 'r')):
    STATE_DATE_COLUMN_NAMES[row[0]]=row[1]
    state_data_attrs[row[0]] = models.CharField(max_length=20)

StateData = type('SateData', (models.Model,), state_data_attrs)

class Column(models.Model):
    code = models.CharField(max_length=50, primary_key = True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return 'Column: %s' % self.code


class Category(models.Model):
    name = models.CharField(max_length=250)


class Categories(models.Model):
    category = models.ForeignKey(Category)
    column = models.ForeignKey(Column)


def _column_fixture():
    for field in StateData._meta.fields:
        if not Column.objects.filter(code=field.name):
            c = Column()
            c.code = field.name
            c.name = STATE_DATE_COLUMN_NAMES.get(field.name, 'EDIT ME IN ADMIN')
            c.description = c.name
            c.save()

_column_fixture()

CODE2STATE_MAP = dict((x.code, x) for x in State.objects.all())
CODE2COLUMN_MAP = dict((x.code, x) for x in Column.objects.all())
