from django.db import models


class WalkTalKie(models.Model):
    model = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255)


class Work(models.Model):
    company_name = models.CharField(max_length=100)


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)


class WalTalKIO(models.Model):
    last = models.IntegerField
    next = models.IntegerField
    date = models.DateTimeField
    walktalkie = models.ForeignKey(WalkTalKie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
