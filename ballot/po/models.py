from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

                                                                                                    # ADDING FIELD TO USERS
 #[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]#
class extra_field(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    validation = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "zzz : donot_edit_anything_here"
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
    votes = models.IntegerField(default=0)

    def __str__(self):
        return 'Name : {}   |   Postion : {}   |   Votes : {}'.format(self.name,self.position,self.votes)

    class Meta:
        verbose_name_plural = "Candidate List"

                                                                                                            # 
#[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]
