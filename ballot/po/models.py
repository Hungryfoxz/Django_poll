from pickle import FALSE
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
# Create your models here. 

                                                                                                    # ADDING FIELD TO USERS
 #[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]#
class extra_field(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    #validation = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Zone_No_Edit"
                                                                                                            # POSITIONS
#[++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]

#creating the positions table..
class Positions(models.Model):
    name = models.CharField(max_length=80)
    priority = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Position List"

                                                                                                            # CANDIDATE
#[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]
#creating the candidates table....
class Candidate(models.Model):
    name = models.CharField(max_length=80)
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    #upload = models.ImageField(upload_to ='uploads/', height_field=None, width_field=None)
    votes = models.IntegerField(default=0)

    

    #def __str__(self):
        #return 'Name : {}   |   Postion : {}   |   Votes : {}'.format(self.name,self.position,self.votes)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = "Candidate List"

                                                                                                            # Total students Voted..
#[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]
# class Voted(models.Model):
#     Total_Students_Voted = models.IntegerField(default=0)

#     def __str__(self):
#         return self.Total_Students_Voted 

#     class Meta:
#         verbose_name_plural = "Zone_Total_Students_Voted"


                                                                                                            # Mock positions..
#[++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]
class Mock_Positions(models.Model):
    name = models.CharField(max_length=80)
    priority = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Table Mock Position"        

                                                                                                            # Mock Poll Table..
#[++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]
class Mock(models.Model):
    name = models.CharField(max_length=80)
    #position = models.CharField( max_length=25, choices=Position_choices)
    position = models.ForeignKey(Mock_Positions, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='static/', height_field=None, width_field=None)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = "Table Mock Poll"