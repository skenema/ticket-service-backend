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
            seats_number = data['seat_number']
            list_of_tickets = []
            for i in seats_number:
                b = Tickets(title=data['title'], seat_number=i, cinema=data['cinema'],
                            showtime=data['showtime'])
                b.save()
                data = {
                    "id": b.pk,
                    "title": b.title,
                    "seat_number": b.seat_number,
                    "cinema": b.cinema,
                    "showtime": b.showtime,
                }
                list_of_tickets.append(data)
            return Response(data={ "tickets": list_of_tickets}, status=status.HTTP_200_OK)
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
        ticket_id = request.query_params.get('ticketId')
        try:
            ticket = Tickets.objects.get(id=ticket_id)
            current_time = datetime.datetime.now()
            ticket_time = datetime.datetime.strptime(
                ticket.showtime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            if current_time > ticket_time:
                return Response({
                    "message": "Ticket expired",
                    "code": "ticket_expired"
                }, status=status.HTTP_403_FORBIDDEN)
            ticket = {
                'id': ticket.id,
                'seatNumber': ticket.seatNumber,
                'cinema': ticket.cinema,
                'showtime': ticket.showtime
            }
        except Tickets.DoesNotExist:
            return Response({
                "message": "Invalid ticket",
                "code": "invalid_ticket"
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(data=ticket, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_ticket(request):
    ticket_id = request.query_params.get('ticketId')
    try:
        ticket = Tickets.objects.get(id=ticket_id)
        ticket.delete()
        return Response(status=status.HTTP_200_OK)
    except Tickets.DoesNotExist:
        return Response({'Invalid': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
