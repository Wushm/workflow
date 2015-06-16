from django.db import models

class ApproveList(models.Model):
	EID = models.CharField(max_length=20)
	ApproveTime = models.DateTimeField()
	VOBBranch = models.CharField(max_length=128)
	RecoverFlag = models.BooleanField()

class ApproveLog(models.Model):
	OpTime = models.DateTimeField()
	EID = models.CharField(max_length=20)
	OpType = models.CharField(max_length=20)  # assign, recover, auto-recover
	VOBBranch = models.CharField(max_length=128)
	IP = models.CharField(max_length=20) # unused
