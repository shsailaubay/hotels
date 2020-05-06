from django.contrib import admin
from .models import LoanApplication, LoanProgram, BlackList, Borrower


admin.site.register(LoanApplication)
admin.site.register(LoanProgram)
admin.site.register(Borrower)
admin.site.register(BlackList)
