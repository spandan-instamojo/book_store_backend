from django.db import models


class HintQuestion(models.Model):
    hint_question = models.CharField(max_length=100)


class StoreUser(models.Model):
    SESSION_KEY = 'store_user_session_id'
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=300)
    address_line1 = models.TextField(blank=True, null=True)
    address_line2 = models.TextField(blank=True, null=True)
    zip_code = models.IntegerField()
    home_phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=False)
    mobile_phone = models.CharField(max_length=20, null=True, blank=True, default='')
    office_phone = models.CharField(max_length=20, null=True, blank=True, default='')

    # handling authentication and active status of the user
    is_authenticated = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # login details
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    hint_question = models.ForeignKey(HintQuestion, on_delete=models.CASCADE)
    hint_answer = models.CharField(max_length=30)

    # timestamp details
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
