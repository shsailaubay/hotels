from loan.models import LoanProgram, BlackList
from datetime import date
from django.utils.translation import ugettext_lazy as _
import urllib.request
import json

import ssl
# У моего мака были проблемы с SSL для urllib
ssl._create_default_https_context = ssl._create_unverified_context


class LoanValidationError(Exception):
    pass


class LoanRequestValidator(object):

    def __init__(self, request):
        self.request = request

    def validate(self):
        raise NotImplementedError


class LoanProgramValidator(LoanRequestValidator):

    def validate(self):
        program = LoanProgram.load()
        if self.request.amount < program.min_sum or self.request.amount > program.max_sum:
            raise LoanValidationError(_("The application does not match the amount"))
        today = date.today()
        birthday = self.request.borrower.birth_date
        borrower_age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if program.max_age < borrower_age or borrower_age < program.min_age:
            raise LoanValidationError(_("The borrower is not suitable for age"))


class LoanGovernmentValidator(LoanRequestValidator):

    def validate(self):
        try:
            data = urllib.request.urlopen(
                "https://stat.gov.kz/api/juridical/gov/?bin={}&lang=ru".format(self.request.borrower.iin)
            )
            request_json = json.loads(data.read().decode('utf-8'))
            print(request_json)
            if request_json.get('success'):
                raise LoanValidationError(_("IIN is an IE"))
        except LoanValidationError as e:
            raise LoanValidationError(str(e))
        except Exception:
            raise LoanValidationError(_("Failed to verify iin"))


class LoanBlackListValidator(LoanRequestValidator):

    def validate(self):
        if BlackList.objects.filter(iin=self.request.borrower.iin).exists():
            raise LoanValidationError(_("Blacklisted Borrower"))

