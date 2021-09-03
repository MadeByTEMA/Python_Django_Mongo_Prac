from email.policy import default

from django.db import models

class ReCafe(models.Model):
    room_excape_cafe_name = models.CharField(max_length=200)
    room_excape_cafe_value = models.CharField(max_length=200)

class ReTheme(models.Model):
    re_cafe = models.ForeignKey(ReCafe, on_delete=models.CASCADE)
    room_excape_theme_name = models.CharField(max_length=200)
    room_excape_theme_value = models.CharField(max_length=200)
    room_excape_cafe_price = models.CharField(max_length=200)
    room_excape_cafe_etc1 = models.CharField(max_length=200)
    room_excape_cafe_etc2 = models.CharField(max_length=200)
    room_excape_cafe_etc3 = models.CharField(max_length=200)
    room_excape_cafe_etc4 = models.CharField(max_length=200)
    room_excape_cafe_etc5 = models.CharField(max_length=200)

class ReTime(models.Model):
    re_theme = models.ForeignKey(ReTheme, on_delete=models.CASCADE)
    room_excape_time_name = models.CharField(max_length=200)
    room_excape_time_value = models.CharField(max_length=200)