from django.core import validators
from django.db import models
from django.contrib.auth.models import User

MINIMUM_ACCOUNT_NUMBER = 1000000
MAXIMUM_ACCOUNT_NUMBER = 9999999


class Account(models.Model):
    user = models.ForeignKey(User)
    balance = models.DecimalField(max_digits=27, decimal_places=2)
    number = models.PositiveIntegerField(unique=True, validators=[validators.MinValueValidator(MINIMUM_ACCOUNT_NUMBER),
                                                                  validators.MaxValueValidator(MAXIMUM_ACCOUNT_NUMBER)])

    def save(self, *args, **kwargs):
        if self.number is None or self.number < MINIMUM_ACCOUNT_NUMBER or self.number > MAXIMUM_ACCOUNT_NUMBER:
            maximum_number = User.objects.all().aggregate(models.Max('number'))['number__max']
            if maximum_number is not None:
                self.number = maximum_number + 1
            else:
                self.number = MINIMUM_ACCOUNT_NUMBER
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.number)


class Transfer(models.Model):
    from_account = models.ForeignKey(Account, related_name='from_account')
    to_account = models.ForeignKey(Account, related_name='to_account')
    amount = models.DecimalField(max_digits=27, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}: ${1} From {2} To {3}'.format(self. timestamp, self.amount, self.from_account, self.to_account)