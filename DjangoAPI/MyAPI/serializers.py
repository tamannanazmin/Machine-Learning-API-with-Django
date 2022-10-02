from rest_framework import serializers
from rest_framework import approvals

class approvalsSerializers(serializers.ModelSerializers):
    class Meta:
        model=approvals
        field='__all__'