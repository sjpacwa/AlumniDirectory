from analytics.basemetric import BaseMetric
from models import Business

class TotalBusiness(BaseMetric):
    uid   = "totalbusiness"
    title = "Total Businesses"

    def calculate(self, start_datetime, end_datetime):
        return Business.objects.filter(timestamp__gte=start_datetime,
            timestamp__lt=end_datetime,business_approved=true).count()

    def get_earliest_timestamp(self):
        try:
            return Business.objects.all().order_by('timestamp')[0].timestamp
        except IndexError:
            return None

class TotalBusinessViews(BaseMetric):
    uid   = "totalbusinessviews"
    title = "Total Business Views"

    def calculate(self, start_datetime, end_datetime):
        sum = 0
        for i in Business.objects.filter(timestamp__gte=start_datetime,timestamp__lt=end_datetime,business_approved=true)
            sum = sum + Business.objects.filter(timestamp__gte=start_datetime,timestamp__lt=end_datetime,business_approved=true)[i].business_num_visit
        return sum

    def get_earliest_timestamp(self):
        try:
            return Business.objects.all().order_by('timestamp')[0].timestamp
        except IndexError:
            return None
