from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Job, Candidate, Skill
from .serializers import JobSerializer, CandidateSerializer, SkillSerializer
from .utils import exception_handler


class GeneralView(APIView):
    """
    Do NOT use this class as a direct view in urls
    """
    model_class = None
    serializer_class = None

    @exception_handler
    def get(self, *args, **kwargs):
        primary_key = kwargs.get("pk")

        if primary_key is None:
            queryset = self.model_class.objects.all()
            serializer = self.serializer_class(queryset, many=True)
        else:
            model_object = self.model_class.objects.get(pk=primary_key)
            serializer = self.serializer_class(model_object, many=False)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @exception_handler
    def put(self, request, *args, **kwargs):
        primary_key = kwargs.get("pk")

        # Request is missing key id
        if primary_key is None:
            return Response({"Error": "Primary key is missing"}, status=status.HTTP_400_BAD_REQUEST)

        model_object = self.model_class.objects.get(pk=primary_key)
        serializer = self.serializer_class(model_object, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @exception_handler
    def delete(self, request, *args, **kwargs):
        primary_key = kwargs.get("pk")

        # Request is missing key id
        if primary_key is None:
            return Response({"Error": "Primary key is missing"}, status=status.HTTP_400_BAD_REQUEST)

        model_object = self.model_class.objects.get(pk=primary_key)

        model_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SkillView(GeneralView):
    model_class = Skill
    serializer_class = SkillSerializer


class JobView(GeneralView):
    model_class = Job
    serializer_class = JobSerializer


class CandidateView(GeneralView):
    model_class = Candidate
    serializer_class = CandidateSerializer


class CandidateMatchView(APIView):

    @exception_handler
    def get(self, *args, **kwargs):
        primary_key = kwargs.get("pk")

        if primary_key is None:
            return Response({"Error": "job id is required!"}, status=status.HTTP_400_BAD_REQUEST)

        # Find job match
        job_object = Job.objects.get(pk=primary_key)
        job_title = job_object.job_title
        job_skills = [str(skill).lower() for skill in job_object.job_skills.all()]

        if not job_title:
            return Response({"Error": "job_title is empty!"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter from all candidates only ones who match the job title
        candidate_queryset = Candidate.objects.filter(candidate_title__iexact=job_title)

        # If the job has not any skills - return all the relevant candidates
        if not job_skills:
            serializer = CandidateSerializer(candidate_queryset, many=True)
            return Response(serializer.data)

        # Find skills match by scores
        skill_candidate_score = {}

        # For each candidate with match for the job title
        for candidate in candidate_queryset:
            # For each skill he has
            for skill in candidate.candidate_skills.all():
                if str(skill).lower() in job_skills:  # If it's match the job skills, He gets one point
                    skill_candidate_score[candidate] = skill_candidate_score.get(candidate, 0) + 1

        # Get the candidate with max score
        final_candidate = max(skill_candidate_score, key=skill_candidate_score.get) if skill_candidate_score else None

        # If score is 0 due to not matching skills - return all relevant candidate
        if not final_candidate:
            serializer = CandidateSerializer(candidate_queryset, many=True)
            return Response(serializer.data)

        # Final candidate-match has found
        serializer = CandidateSerializer(final_candidate, many=False)
        return Response(serializer.data)
