from django.db import models

class State(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return 'State: %s' % self.code


class StateData(models.Model):
    
    state = models.ForeignKey(State)
    year = models.PositiveSmallIntegerField()
    en_coal = models.CharField(max_length=10)
    en_gas = models.CharField(max_length=10)

    def __unicode__(self):
        return 'StateData: %s' % self.state.code


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

CODE2STATE_MAP = dict((x.code, x) for x in State.objects.all())
CODE2COLUMN_MAP = dict((x.code, x) for x in Column.objects.all())
