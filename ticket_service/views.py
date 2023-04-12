from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tickets


@api_view(['GET'])
def get_ticket(request):
    if request.method == 'GET':
        tickets = Tickets.objects.all()
        ticket_list = []
        for i in tickets:
            ticket = {
                'id': i.id,
                'title': i.title,
                'seatNumber': i.seatNumber,
                'cinema': i.cinema,
                'showtime': i.showtime
            }
            ticket_list.append(ticket)
        return Response(data=ticket_list, status=200, content_type='application/json')

@api_view(['GET'])
def validate_ticket(request):
    if request.method == 'GET':
        ticket_id = request.query_params.get('ticketid')
        print(ticket_id)
        try:
            user = Tickets.objects.get(id=ticket_id)
            print(user)
            ticket = {
                'id': user.id,
                'title': user.title,
                'seatNumber': user.seatNumber,
                'cinema': user.cinema,
                'showtime': user.showtime
            }
        except Tickets.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        return Response(data=ticket, status=200, content_type='application/json')
