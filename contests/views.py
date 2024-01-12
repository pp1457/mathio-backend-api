from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import generics, status
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from . import serializers
from .models import Contest,Problem
from authentication.models import UserProfile, UserContest

from random import randint
from multi_elo import EloPlayer, calc_elo



class EndContestView(APIView):
    def post(self, request, contest_id):
        contest = get_object_or_404(Contest, id=contest_id)

        now = timezone.now()
        if now > contest.end_time:
            # Calculate ranking based on the rated_score field
            participants = contest.usercontest_set.all().order_by('-rated_score')
            for i, participant in enumerate(participants, start=1):
                participant.rank = i
                participant.save()

            # Use multi_elo library to calculate and save rating changes
            elo_players = [EloPlayer(place=participant.rank, elo=participant.user_profile.rating)
                           for participant in participants]

            k_factor = 16  # Adjust this according to your requirements

            new_elos = calc_elo(elo_players, k_factor)

            for i, participant in enumerate(participants):
                participant.user_profile.rating = new_elos[i]
                participant.user_profile.save()

            return Response({'success': True, 'message': 'Contest ended successfully.'}, status=status.HTTP_200_OK)

        return Response({'success': False, 'message': 'Contest has not ended yet.'}, status=status.HTTP_400_BAD_REQUEST)



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
                        user_contest.rated_score += problem.score

                    user_contest.unrated_score += problem.score

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

class CreateContestView(generics.CreateAPIView):
    serializer_class = serializers.CreateContestSerializer
    permission_classes = [IsAdminUser]


class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = serializers.ProblemListSerializer

class ProblemDetailView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = serializers.ProblemDetailSerializer


class AddProblemView(generics.CreateAPIView):
    serializer_class = serializers.AddProblemSerializer
    permission_classes = [IsAdminUser]


    def perform_create(self, serializer):
        # Get the contest_id from the URL
        contest_id = self.kwargs.get('contest_id')
        
        # Get the Contest instance or return a 404 response if not found
        contest = get_object_or_404(Contest, pk=contest_id)

        # Set the contest field in the serializer with the retrieved Contest instance
        serializer.save(contest=contest)

class ContestProblemListView(APIView):
    def get(self, request, contest_id):
        contest = get_object_or_404(Contest, id=contest_id)
        problems = Problem.objects.filter(contest__id=contest_id)

        serializer = serializers.ProblemListSerializer(problems, many=True)

        return Response({'problem_ids': serializer.data})
