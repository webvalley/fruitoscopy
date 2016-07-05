from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    label = models.SmallIntegerField()
    gps = models.TextField(null=True)
    tmstp = models.DateTimeField(null=True) # Timestamp
    # image_path = models.TextField(blank=True, null=True) # I'm not expecting the pickers to take a pic of every sample they scan, hence default=None
    ml_model = models.ForeignKey(ML_Model, on_delete=models.PROTECT)
    sp_model = models.ForeignKey(SP_Model, on_delete=models.PROTECT)

    def __string__(self):
        return self.spectrum