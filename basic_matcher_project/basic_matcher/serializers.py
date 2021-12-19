from rest_framework import serializers
from basic_matcher.models import Job, Candidate, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'skill_name')


class JobSerializer(serializers.ModelSerializer):
    job_skills = SkillSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Job
        fields = ('id', 'job_title', 'job_skills')

    def create(self, validated_data):
        if not validated_data.get("job_skills"):
            return super(JobSerializer, self).create(validated_data)

        # Remove Skills list from request data
        job_skills = validated_data.pop('job_skills')

        # Create objects per skill
        skills_list = []
        for skill in job_skills:
            skills_list.append(Skill.objects.create(skill_name=skill['skill_name']))

        # Create Job object based on the later
        job = Job.objects.create(**validated_data)

        # Append the skills_list to job object
        job.job_skills.set(skills_list)

        return job


class CandidateSerializer(serializers.ModelSerializer):
    candidate_skills = SkillSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Candidate
        fields = ('id', 'candidate_name', 'candidate_title', 'candidate_skills')

    def create(self, validated_data):
        if not validated_data.get("candidate_skills"):
            return super(CandidateSerializer, self).create(validated_data)

        # Remove Skills list from request data
        job_skills = validated_data.pop('candidate_skills')

        # Create objects per skill
        skills_list = []
        for skill in job_skills:
            skills_list.append(Skill.objects.create(skill_name=skill['skill_name']))

        # Create Candidate object based on the later
        candidate = Candidate.objects.create(**validated_data)

        # Append the skills_list to job object
        candidate.job_skills.set(skills_list)

        return candidate
