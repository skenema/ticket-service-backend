from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tickets
import datetime

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
        try:
            user = Tickets.objects.get(id=ticket_id)
            current_time = datetime.datetime.now()
            if current_time > user.showtime:
                return Response({'Expired': 'You ticked isexpired'}, status=200)
            ticket = {
                'id': user.id,
                'title': user.title,
                'seatNumber': user.seatNumber,
                'cinema': user.cinema,
                'showtime': user.showtime
            }
        except Tickets.DoesNotExist:
            return Response({'error': 'Ticket Invalid'}, status=404)
        return Response(data=ticket, status=200, content_type='application/json')
