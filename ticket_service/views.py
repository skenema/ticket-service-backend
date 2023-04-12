from django.shortcuts import render
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
                'seatNumber': i.seatNumber,
                'cinema': i.cinema,
                'showtime': i.showtime
            }
            ticket_list.append(ticket)
        return Response(data=ticket_list, status=200)

@api_view(['GET'])
def validate_ticket(request):
    if request.method == 'GET':
        ticket_id = request.query_params.get('ticketid')
        try:
            ticket = Tickets.objects.get(id=ticket_id)
            current_time = datetime.datetime.now()
            if current_time > ticket.showtime:
                return Response({'Expired': 'You ticked isexpired'}, status=403)
            ticket = {
                'id': ticket.id,
                'seatNumber': ticket.seatNumber,
                'cinema': ticket.cinema,
                'showtime': ticket.showtime
            }
        except Tickets.DoesNotExist:
            return Response({'Invalid': 'Ticket Invalid'}, status=404)
        return Response(data=ticket, status=200)
