from django.db import models

# Create your models here.
    
class Admin_reg(models.Model):
    admin_name = models.CharField(max_length=100)
    admin_mail=models.EmailField(max_length=50,unique=True)
    password = models.CharField(max_length=30)
    def __str__(self):
        return self.admin_name
    
class User_signup(models.Model):
    Emp_name=models.CharField(max_length=100)
    Emp_id=models.IntegerField(unique=True)
    Sys_id=models.IntegerField(unique=True)
    Emp_email=models.EmailField(max_length=50,unique=True)
    emp_password=models.CharField(max_length=20)
    
    def __str__(self):
        return self.Emp_name
    
class Agent_signup(models.Model):
    agent_name = models.CharField(max_length=100, unique=True, null=False)
    agent_id=models.CharField(max_length=20,unique=True)
    agent_mail = models.EmailField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=128)
    
    def __str__(self):
        return self.agent_name
    
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    CATEGORY_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Network', 'Network'),
        ('Other', 'Other'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User_signup, on_delete=models.CASCADE)
    assigned_agent = models.ForeignKey(Agent_signup, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Low') 
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True) 
    
    seen_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen_by_agent = models.BooleanField(default=False)


class TicketFeedback(models.Model):
    user = models.ForeignKey(User_signup, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1 - Poor'), (2, '2'), (3, '3 - Okay'), (4, '4'), (5, '5 - Excellent')])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
