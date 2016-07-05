from django.db import models
from django.contrib.postgres.fields import ArrayField
from tables.choices import RIPENESS_CHOICES

# Machine Learning models
class ML_Model(models.Model):

    vals = models.TextField()

    def __string__(self):
        return self.path


#Signal Processing algorithms
class SP_Model(models.Model):

    vals = models.TextField()

    def __string__(self):
        return self.path

# Samples
class Sample(models.Model):

    spectrum = ArrayField(models.FloatField())
    fruit = models.IntegerField()
    label = models.SmallIntegerField(choices=RIPENESS_CHOICES)
    gps = models.TextField(null=True)
    tmstp = models.DateTimeField(null=True) # Timestamp
    # TODO: add Image Class
    # image_path = models.TextField(blank=True, null=True) # I'm not expecting the pickers to take a pic of every sample they scan, hence default=None
    label_is_right = models.BooleanField(default=False)
    ml_model = models.ForeignKey(ML_Model, on_delete=models.PROTECT)
    sp_model = models.ForeignKey(SP_Model, on_delete=models.PROTECT)

    def __string__(self):
        return self.spectrum