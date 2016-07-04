from django.db import models

# Machine Learning models
class ML_model(models.Model):
    def __string__(self):
        return self.path
    vals = models.TextField() # TODO: ask about how those values will be passed/stored

#Signal Processing algorithms
class SP_model(models.Model):
    def __string__(self):
        return self.path
    vals = models.TextField()

# Spectrum
class Sample(models.Model):
    def __string__():
        return self.spectrum
    spectrum = models.TextField()
    fruit = models.TextField()
    label = models.IntegerField(max_digits=2) # ripe, not ripe, too ripe
    gps = models.TextField()
    tmstp = models.IntegerField()
    ml_model = models.ForeignKey(ML_model, on_delete=models.PROTECT)
    sp_model = models.ForeignKey(SP_model, on_delete=models.PROTECT)
