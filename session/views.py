from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from _config.utils import uuid_filepath

from .models import MultiplyerData, RespiratoryGraphData, SustainedAttentionData


def index(request):
    return render(request, "session/index.html")


def rg_record(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            rg_obj = RespiratoryGraphData()

            # Write user and time
            rg_obj.user = request.user
            rg_obj.date_created = timezone.now()

            # Retrieve data from request
            csv_input = request.POST["csv_input"]
            time_input = request.POST["time_input"]
            note_input = request.POST["note_input"]

            # Write CSV data
            from urllib.parse import unquote

            file_path = uuid_filepath(rg_obj, "result.csv")
            rg_obj.csv_data.save(file_path, ContentFile(unquote(csv_input)))

            # Import MultiplyerData
            from django.core.exceptions import ObjectDoesNotExist

            try:
                mul_obj = MultiplyerData.objects.get(user=request.user)
            except ObjectDoesNotExist:
                mul_obj = MultiplyerData.objects.create(user=request.user)

            # Update Multiplyer date and amount
            from datetime import datetime, time, timedelta

            time_now = datetime.now()
            time_yesterday = time_now - timedelta(days=1)
            
            time_pivot_yd = datetime.combine(time_yesterday.date(), time(17, 0))
            time_pivot_am = datetime.combine(time_now.date(), time(5, 0))
            time_pivot_pm = datetime.combine(time_now.date(), time(17, 0))

            # Update daily multiplyer
            if time_now > time_pivot_pm and time_now != time_pivot_pm:
                mul_obj.daily_datetime = time_pivot_pm
                mul_obj.daily_tokens = 900
            elif time_now > time_pivot_am and time_now != time_pivot_am:
                mul_obj.daily_datetime = time_pivot_am
                mul_obj.daily_tokens = 900
            elif time_now != time_pivot_yd:
                mul_obj.daily_datetime = time_pivot_yd
                mul_obj.daily_tokens = 900
                
            # Update hourly multiplyer
            if time_now - mul_obj.hourly_datetime > timedelta(hours=1):
                mul_obj.hourly_datetime = time_now
                mul_obj.hourly_tokens = 300
            
            # Calculate multiplied score
            score = 0
            tokens_required = int(float(time_input))
            
            # Use hourly tokens
            tokens_used = min(tokens_required, mul_obj.hourly_tokens)
            score += tokens_used * (1/6) * 3
            tokens_required -= tokens_used
            mul_obj.hourly_tokens -= tokens_used
            
            # Use daily tokens
            tokens_used = min(tokens_required, mul_obj.daily_tokens)
            score += tokens_used * (1/6) * 3
            tokens_required -= tokens_used
            mul_obj.daily_tokens -= tokens_used
            
            # Add remainder
            score += tokens_required * (1/6)

            # Write score data
            rg_obj.score = score

            # Write note data
            rg_obj.note = note_input

            # Save into model
            mul_obj.save()
            rg_obj.save()

    return render(request, "session/rg-record.html")


@login_required(login_url="common:login")
def rg_inquiry(request, username):
    user = User.objects.get(username=username)

    # Process inquiry only if user matches
    if request.user == user:
        # Initial variable settings
        data_list = []
        csv_x_data_list = []
        csv_y_data_list = []

        # Load all data if user is staff
        if user.is_staff:
            raw_data_list = RespiratoryGraphData.objects.all().order_by("-date_created")
        # If not, load user data only
        else:
            raw_data_list = RespiratoryGraphData.objects.filter(user=user).order_by(
                "-date_created"
            )

        # Paginate raw datas
        page = request.GET.get("page", 1)
        paginator = Paginator(raw_data_list, 10)
        raw_data_list = paginator.get_page(page)

        for data in raw_data_list:
            from _config.settings.base import MEDIA_ROOT
            import csv

            csv_x_data = []
            csv_y_data = []

            with open(f"{MEDIA_ROOT}/{data.csv_data}", "r") as file:
                csv_data = csv.reader(file)
                for row in csv_data:
                    csv_x_data.append(float(row[0]))
                    csv_y_data.append(float(row[1]))

            csv_x_data_list.append(csv_x_data)
            csv_y_data_list.append(csv_y_data)

            data_list = zip(raw_data_list, csv_x_data_list, csv_y_data_list)

        # Send context to inquiry html template
        context = {
            "data_list": data_list,
            "page_obj": raw_data_list,
        }
        return render(request, "session/rg-inquiry.html", context)

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)


@login_required(login_url="common:login")
def rg_delete(request, id):
    target_data = RespiratoryGraphData.objects.get(id=id)

    # Process delete only if user matches
    if target_data.user == request.user:
        target_data.delete()
        return redirect("session:rg-inquiry", request.user)

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)
