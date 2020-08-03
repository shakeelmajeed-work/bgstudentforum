from django.db import models


class ad(models.Model):
    ad_link = models.URLField(max_length=2000)
    image = models.ImageField(upload_to="ads/")

    def __str__(self):
        return self.ad_link
