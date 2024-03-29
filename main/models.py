from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
import uuid

EVENT_POINTS = 10 # points attained for attending an event
MEETING_POINTS = 5 # points attained for attending a meeting
TIER_STANDARDS = {
        'Platinum': 80,
        'Gold': 60,
        'Silver': 45,
        'Bronze': 30,
        'Beginner': 0

    } 

TIERS_DATA = [
        {'name': 'Platinum', 'points': 80, 'description': open('main/platinum.txt', 'r+').read()},
        {'name': 'Gold', 'points': 60, 'description': open('main/gold.txt', 'r+').read()},
        {'name': 'Silver', 'points': 45, 'description': open('main/silver.txt', 'r+').read()},
        {'name': 'Bronze', 'points': 30, 'description': open('main/bronze.txt', 'r+').read()},
        {'name': 'Beginner', 'points': 0, 'description': open('main/beginner.txt', 'r+').read()}
    ]




class Semester(models.Model):
    ''' Model to represent a semester '''
    POT_CHOICES = [

        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    ]
    part_of_term = models.CharField(max_length=20, choices=POT_CHOICES, default='Fall') # e.g. 'Fall 2022'
    year = models.CharField(max_length=10, default='2022')
    

    def __str__(self):
        return '{} {}'.format(self.part_of_term, self.year)

class CustomUser(AbstractBaseUser, PermissionsMixin):


    email = models.EmailField(_('email address'), unique=True)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    bonus_points = models.IntegerField(default=0, blank=True, null=True) # bonus points received for various things

    is_eboard = models.BooleanField(default=False)

    POSITION_CHOICES = [

        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Vice President of Administration', 'Vice President of Administration'),
        ('Vice President of Finance', 'Vice President of Finance')

    ]

    position = models.CharField(max_length=80, choices=POSITION_CHOICES, blank=True, null=True)

 
    membership_points = models.IntegerField(default=0) # total membership points for member

    TIER_CHOICES = [

        ('Platinum', 'Platinum'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Bronze', 'Bronze'),
        ('Beginner', 'Beginner')
    ]

    membership_tier = models.CharField(max_length=12, choices=TIER_CHOICES, default='Beginner', blank=True, null=True)

    YEAR_IN_SCHOOL_CHOICES = [
    ('Freshman', 'Freshman'),
    ('Sophomore', 'Sophomore'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
    ('Graduate', 'Graduate'),
    ]

    year_in_school = models.CharField(max_length=12, choices=YEAR_IN_SCHOOL_CHOICES, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_update_membership_points(self):
        # below commented method doesnt allow for events to have different point values
        # self.membership_points = EVENT_POINTS * self.event_set.count() + MEETING_POINTS * self.meeting_set.count()

        points = 0
        curr_semester = get_curr_semester()
        # add all event points
        for event in self.event_set.all():
            if event.semester == curr_semester:
                points += event.points
        # add all meeting points
        for meeting in self.meeting_set.all():
            if meeting.semester == curr_semester:
                points += meeting.points

        try:
            points += self.bonus_points # add bonus points to member's membership_points
        except:
            print("no membership points for user")

        self.membership_points = points
        self.save()
        return self.membership_points

    def get_update_membership_tier(self):

        if self.membership_points >= TIER_STANDARDS['Platinum']:
            self.membership_tier = 'Platinum'

        elif self.membership_points >= TIER_STANDARDS['Gold']:
            self.membership_tier = 'Gold'

        elif self.membership_points >= TIER_STANDARDS['Silver']:
            self.membership_tier = 'Silver'

        elif self.membership_points >= TIER_STANDARDS['Bronze']:
            self.membership_tier = 'Bronze'

        else:
            self.membership_tier = 'Beginner'
        self.save()
        return self.membership_tier

    def is_eboard_to_str(self):
        if self.is_eboard:
            return "Yes"
        return "No"




class Event(models.Model):
    ''' Model to represent our events '''
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    google_drive_folder_id = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    organizers = models.ManyToManyField(CustomUser, related_name='event_organizers', related_query_name='event_organizers')
    date_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True) # room number
    attendees = models.ManyToManyField(CustomUser)
    points = models.IntegerField(default=EVENT_POINTS)

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    ''' Model to represent our weekly meetings '''
    google_drive_folder_id = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=10, default='')
    organizers = models.ManyToManyField(CustomUser, related_name='meeting_organizers', related_query_name='meeting_organizers')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(CustomUser)
    points = models.IntegerField(default=MEETING_POINTS)

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "{} Meeting".format(self.date_time)



class SemesterMembershipStorage(models.Model):
    ''' Model to store membership points and tiers of previous semesters '''
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=0)
    membership_points = models.IntegerField(default=0)
    membership_tier = models.CharField(max_length=12, default='', blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.user.email, str(self.semester))

def get_curr_semester():
    # THIS MUST BE UPDATED TO THE CURRENT SEMESTER
    # Whatever semester this returns is the one for which points are calculated 
    CURR_PART_OF_TERM = "Spring"
    CURR_YEAR = '2023'
    return Semester.objects.get(part_of_term=CURR_PART_OF_TERM, year=CURR_YEAR)
