from django.db import models
from core.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

'''
class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    message = models.CharField(max_length=500, blank=True)
    owner = models.ForeignKey(
        User, related_name="leads", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
'''


class SemesterManager(models.Manager):

    def get_by_natural_key(self, semester, year):
        print("get_by_natural_key semester:", year, semester)
        return self.get(year=year, semester=semester)

    def get_by_natural_key(self, year, semester):
        print("get_by_natural_key semester:", year, semester)
        return self.get(year=year, semester=semester)

    #def natural_key(self):
    #    return self.year, self.semester


# Set the semester as a separate model/table
# of year + semester: A, B
class Semester(models.Model):

    class Meta:
        db_table = "cfp_semester"
        unique_together = (("year", "sem"),)

    year = models.IntegerField(validators=[MinValueValidator(2019), MaxValueValidator(2040)])
    sem = models.CharField(max_length=1, choices=(("A", "A"), ("B", "B")))

    def __str__(self):
        return '%4d%s' % (self.year, self.sem)

    #objects = SemesterManager()

# Call of Proposals model
# This represents the table entry for
# semester
# start of call date
# close of call date
class CfP(models.Model):

    class Meta:
        db_table = "cfp_dates"
        unique_together = ("pi", "semester")

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # the PI will be our own core.models.User
    # the related_name is just a helper.
    # Django automatically creates a method to relate this model to the user
    # model.
    # E.g.
    # User.cfp_set.all()
    # By setting the related_name, say cfp_entry this will also be valid
    # User.cfp_entry.all()
    pi = models.ForeignKey(User, related_name="CfP_entry", on_delete=models.DO_NOTHING)
    open = models.DateTimeField(blank=True, null=True)
    close = models.DateTimeField(blank=True, null=True)
    tz = models.CharField(max_length=40, null=True, blank=True)
