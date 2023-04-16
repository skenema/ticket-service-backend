from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tickets
import datetime
from django.core import serializers
import json

@api_view(['POST'])
def create_ticket(request):
    if request.method == "POST":
        b = Tickets(seatNumber="test", cinema="test", showtime=datetime.datetime.now())
        b.save()
        data = {
            "id": b.pk,
            "seatNumber": b.seatNumber,
            "cinema": b.cinema,
            "showtime": b.showtime,
            "validate": "test"
        }
        return Response(data=data, status=status.HTTP_200_OK)

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
        return Response(data=ticket_list, status=status.HTTP_200_OK)

@api_view(['GET'])
def validate_ticket(request):
    if request.method == 'GET':
        ticket_id = request.query_params.get('ticketid')
        try:
            ticket = Tickets.objects.get(id=ticket_id)
            current_time = datetime.datetime.now()
            ticket_time = datetime.datetime.strptime(ticket.showtime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            if current_time > ticket_time:
                return Response({'Expired': 'You ticked isexpired'}, status=status.HTTP_200_OK)
            ticket = {
                'id': ticket.id,
                'seatNumber': ticket.seatNumber,
                'cinema': ticket.cinema,
                'showtime': ticket.showtime
            }
        except Tickets.DoesNotExist:
            return Response({'Invalid': 'Ticket Invalid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=ticket, status=status.HTTP_200_OK)

# for develop
@api_view(['DELETE'])
def delete_ticket(request):
    ticket_id = request.query_params.get('ticketid')
    try:
        ticket = Tickets.objects.get(id=ticket_id)
        ticket.delete()
        return Response(status=status.HTTP_200_OK)
    except Tickets.DoesNotExist:
        return Response({'Invalid': 'NOt found'}, status=status.HTTP_404_NOT_FOUND)