from django.db import models

class Leave(models.Model):
    leave_type = models.CharField(max_length=30)
    leave_slug = models.SlugField(max_length=30, unique=True)
    leave_description = models.CharField(max_length=300)
    total_leaves_given = models.IntegerField()

    def __str__(self):
        return self.leave_type

class Application(models.Model):
    pending = "P"
    approved = "A"
    rejected = "R"
    status_choice = [
        (pending, 'PENDING'),
        (approved, 'APPROVED'),
        (rejected, 'REJECTED'),
    ]

    employee_id = models.CharField(max_length=100)
    email = models.EmailField()
    pub_date = models.DateField(auto_now_add=True)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    remark = models.CharField(max_length=300)
    approval = models.CharField(max_length=1, choices=status_choice,  default=pending)
    hr_remark = models.CharField(max_length=100, default="NA", blank=True)

    def __str__(self):
        return self.email + " " + self.remark

    class Meta:
        ordering = ['pub_date']