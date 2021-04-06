from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


def welcome_view(request):
    return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "menu.html", context={})


line_of_cars = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": []
    }
curr_ticket = 0
next_ticket = None


def get_service_lens():
    global line_of_cars

    oil_len = len(line_of_cars["change_oil"])
    tire_len = len(line_of_cars["inflate_tires"])
    diagnostic_len = len(line_of_cars["diagnostic"])

    return oil_len, tire_len, diagnostic_len


class TicketView(View):
    def get(self, request, service, *args, **kwargs):
        global line_of_cars, curr_ticket

        oil_time = 2
        tire_time = 5
        diagnostic_time = 30

        curr_ticket += 1

        oil_len, tire_len, diagnostic_len = get_service_lens()

        oil_wait = oil_len * oil_time
        tire_wait = tire_len * tire_time
        diagnostic_wait = diagnostic_len * diagnostic_time

        if curr_ticket == 3:
            if oil_wait:
                curr_wait = oil_time
            elif tire_wait:
                curr_wait = tire_time
            else:
                curr_wait = diagnostic_time

        elif curr_ticket > 3:
            curr_wait = oil_wait + tire_wait + diagnostic_wait

        else:
            curr_wait = 0

        if "oil" in service:
            line_of_cars["change_oil"].append(curr_ticket)
        elif "tires" in service:
            line_of_cars["inflate_tires"].append(curr_ticket)
        else:
            line_of_cars["diagnostic"].append(curr_ticket)


        return render(request, "ticket_queue.html", context={"curr_ticket": curr_ticket, "curr_wait": curr_wait})


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        global line_of_cars

        oil_len, tire_len, diagnostic_len = get_service_lens()

        return render(request, "processing.html", context={"oil_len": oil_len, "tire_len": tire_len, "diagnostic_len": diagnostic_len})

    def post(self, request, *args, **kwargs):
        global line_of_cars, next_ticket

        oil_len, tire_len, diagnostic_len = get_service_lens()

        if oil_len:
            next_ticket = line_of_cars["change_oil"].pop(0)
        elif tire_len:
            next_ticket = line_of_cars["inflate_tires"].pop(0)
        elif diagnostic_len:
            next_ticket = line_of_cars["diagnostic"].pop(0)

        return redirect("/next")


class NextView(View):
    def get(self, request, *args, **kwargs):
        global next_ticket, line_of_cars

        return render(request, "next.html", context={"next_ticket": next_ticket, "line_of_cars": line_of_cars})

