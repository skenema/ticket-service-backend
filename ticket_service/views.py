from django.shortcuts import render
import jsonschema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tickets
import datetime
from .schema import ticket_schema
import json


@api_view(['POST'])
def create_ticket(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
            jsonschema.validate(data, ticket_schema)
            b = Tickets(title=data['title'],seat_number=data['seat_number'], cinema=data['cinema'],
                        showtime=data['showtime'])
            base_url = request.build_absolute_uri().split('/')
            prefix_url = base_url[:-1]
            b.save()
            prefix_url.append(f'validate-ticket?ticketid={b.pk}')
            valdiate_url = '/'.join(prefix_url)
            data = {
                "id": b.pk,
                "seatNumber": b.seat_number,
                "cinema": b.cinema,
                "showtime": b.showtime,
                "validate": valdiate_url
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except jsonschema.exceptions.ValidationError as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_ticket(request):
    if request.method == 'GET':
        tickets = Tickets.objects.all()
        ticket_list = []
        for i in tickets:
            ticket = {
                'id': i.id,
                'title': i.title,
                'seat_number': i.seat_number,
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

@api_view(['DELETE'])
def delete_ticket(request):
    ticket_id = request.query_params.get('ticketid')
    try:
        ticket = Tickets.objects.get(id=ticket_id)
        ticket.delete()
        return Response(status=status.HTTP_200_OK)
    except Tickets.DoesNotExist:
        return Response({'Invalid': 'NOt found'}, status=status.HTTP_404_NOT_FOUND)