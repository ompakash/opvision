from django.db import models

class FeatureDetection(models.Model):
    image = models.ImageField(upload_to="FeatureDetection/images")