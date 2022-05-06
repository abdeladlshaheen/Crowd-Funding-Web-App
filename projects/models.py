from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Rate(models.Model):
    class RateChoices(models.IntegerChoices):
        POOR = 1
        FAIR = 2
        GOOD = 3
        VERYGOOD = 4
        EXCELLENT = 5

    rate = models.IntegerField(
        choices=RateChoices.choices, unique=True, primary_key=True)

    def __str__(self):
        return f"Rate ({self.rate})"


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    details = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    # store numbers up to approximately one billion
    total_target = models.DecimalField(decimal_places=3, max_digits=19)
    donations = models.DecimalField(default=0, decimal_places=3, max_digits=19)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    thumbnail = models.ImageField(
        blank=True, null=True, upload_to="projects/static/images")
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass


class UserRateProject(models.Model):
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Picture(models.Model):
    picture = models.ImageField(
        blank=True, null=True, upload_to="projects/static/images")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
