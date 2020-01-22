from django.db import models

# Create your models here.

class Ind_User(models.Model):
    username = models.CharField(max_length=100)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    e_file = models.FileField(upload_to='uploads/', default='Ind_User_Data.xlsx')

class Org_User(models.Model):
    username = models.CharField(max_length=100)
    c_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    e_file_1 = models.FileField(upload_to='uploads/', default='Org_User_Data_1.xlsx')
    e_file_2 = models.FileField(upload_to='uploads/', default='Org_User_Data_2.xlsx')
    e_file_3 = models.FileField(upload_to='uploads/', default='Org_User_Data_3.xlsx')
    e_file_4 = models.FileField(upload_to='uploads/', default='Org_User_Data_4.xlsx')


