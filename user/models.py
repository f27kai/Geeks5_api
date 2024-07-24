from django.db import models

class SmsCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='sms')

    def __str__(self):
        return f"SMS Code for {self.user}"
