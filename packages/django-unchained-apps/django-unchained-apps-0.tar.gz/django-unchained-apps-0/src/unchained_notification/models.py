from django.contrib.auth import get_user_model
from django.db import models
from fcm_django.models import FCMDevice


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), blank=True, on_delete=models.CASCADE, db_constraint=False)
    text = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    payload = models.TextField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def send_notification(self):
        if self.user.exists():
            devices = FCMDevice.objects.filter(user_id__in=list(self.user.values_list('id', flat=True)),
                                               active=True)
        else:
            devices = FCMDevice.objects.filter(active=True)
        devices.send_message(title=self.title, body=self.text, sound=True,
                             data={"category": self.type, 'payload': self.payload},
                             extra_kwargs={
                                 "actions": [
                                     {
                                         "title": "Accept",
                                         "action": "accept",
                                         "icon": "icons/heart.png"
                                     },
                                     {
                                         "title": "Ignore",
                                         "action": "ignore",
                                         "icon": "icons/cross.png"
                                     }
                                 ]})

    def __str__(self):
        return "%s. %s" % (self.id, self.text)
