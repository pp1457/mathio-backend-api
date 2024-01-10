from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from .models import Contest,Problem
from authentication.models import UserProfile, UserContest
from rest_framework import generics
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from . import serializers


@permission_classes([IsAuthenticated])
class SubmitAnswerView(APIView):
    def post(self, request, contest_id, problem_id):
        serializer = serializers.SubmitAnswerSerializer(data=request.data)
        if serializer.is_valid():
            user_answer = serializer.validated_data.get('user_answer')
            
            current_time = timezone.now()
            user = request.user
            contest = get_object_or_404(Contest, id=contest_id)
            problem = get_object_or_404(Problem, id=problem_id)

            # Get or create UserProfile for the user
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Get or create UserContest for the user in the specified contest
            user_contest, created = UserContest.objects.get_or_create(user_profile=user_profile, contest=contest)

            if user_answer == problem.answer:
                # Check if the problem is already solved by the user in the contest
                if problem not in user_contest.solved_problems.all():
                    # Update the UserProfile and UserContest based on the submission
                    user_contest.solved_problems.add(problem)

                    if contest.start_time <= current_time <= contest.end_time:
                        # Update rating
                        user_profile.rating += 100

                    # Save the changes
                    user_profile.save()
                    user_contest.save()

                    return Response({'status': 'success', 'message': 'Answer submitted successfully'})
                else:
                    return Response({'status': 'error', 'message': 'Problem already solved'})
            else:
                return Response({'status': 'error', 'message': 'Incorrect answer'})
        else:
            return Response({'status': 'error', 'message': 'Invalid data'})



class ContestListView(generics.ListAPIView):
    queryset = Contest.objects.all()
    serializer_class = serializers.ContestSerializer

class ContestDetailView(generics.RetrieveAPIView):
    queryset = Contest.objects.all()
    serializer_class = serializers.ContestSerializer

class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = serializers.ProblemListSerializer

class ProblemDetailView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = serializers.ProblemDetailSerializer

class ContestProblemListView(APIView):
    def get(self, request, contest_id):
        contest = get_object_or_404(Contest, id=contest_id)
        problems = Problem.objects.filter(contest__id=contest_id)

        serializer = serializers.ProblemListSerializer(problems, many=True)

        return Response({'problem_ids': serializer.data})
