from rest_framework.generics import CreateAPIView
from .models import LoanApplication, LoanProgram
from .serialaizers import LoanApplicationSerializer
from rest_framework.response import Response
from rest_framework import status
from .loan_validators import LoanProgramValidator, LoanGovernmentValidator, LoanBlackListValidator, LoanValidationError


class LoanRequestView(CreateAPIView):
    serializer_class = LoanApplicationSerializer
    queryset = LoanApplication
    loan_validators = [
        LoanProgramValidator,
        LoanGovernmentValidator,
        LoanBlackListValidator
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        try:
            for validator in self.loan_validators:
                validator_obj = validator(instance)
                validator_obj.validate()
        except LoanValidationError as e:
            instance.rejection_reason = str(e)
            instance.status = LoanApplication.REJECTED
        else:
            instance.status = LoanApplication.ACCEPTED
        instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

