from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.skill_name


class Job(models.Model):
    job_title = models.CharField(max_length=50, unique=True)
    job_skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)

    def __str__(self):
        return self.job_title


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=50)
    candidate_title = models.CharField(max_length=50)
    candidate_skills = models.ManyToManyField(Skill, related_name='candidates', blank=True)

    def __str__(self):
        return f"{self.candidate_name}, {self.candidate_title}"
