import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Patent
from .serializers import PatentSerializer
from django.core.cache import cache
from django.utils.decorators import method_decorator
import hashlib  # To generate unique cache keys


@api_view(['GET'])
def summary_view(request):
    # Define cache key (unique for this view)
    cache_key = 'summary_view_cache'
    cached_data = cache.get(cache_key)

    # Return cached data if it exists
    if cached_data:
        return Response(cached_data, status=status.HTTP_200_OK)

    try:
        # Fetch all patent data
        patents = Patent.objects.all()
        if not patents.exists():
            return Response({"error": "No patent data available"}, status=status.HTTP_404_NOT_FOUND)

        # Convert to DataFrame for analysis
        df = pd.DataFrame(list(patents.values()))

        # Check if dataframe is empty
        if df.empty:
            return Response({"error": "No data available"}, status=status.HTTP_404_NOT_FOUND)


        # Basic summary statistics
        summary_stats = {
            'mean_pages': df['pages'].mean(),
            'median_pages': df['pages'].median(),
            'std_pages': df['pages'].std(),
            'applicant_name_counts': df['applicant_name'].value_counts().to_dict(),
            'relevancy_stats': df['relevancy'].describe().to_dict(),
        }

        response_data = {
            "summary_statistics": summary_stats,
        }

        # Cache the result for 10 minutes (600 seconds)
        cache.set(cache_key, response_data, timeout=600)

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def query_view(request):
    try:
        # Generate a unique cache key based on query parameters
        query_params = request.GET.dict()
        cache_key = f"query_view_{hashlib.md5(str(query_params).encode()).hexdigest()}"
        cached_data = cache.get(cache_key)

        # Return cached data if it exists
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # Extract query parameters from the URL
        id = request.GET.get('id', None)
        source = request.GET.get('source', None)
        date_published = request.GET.get('date_published', None)
        pages_min = request.GET.get('pages_min', None)
        pages_max = request.GET.get('pages_max', None)
        title = request.GET.get('title', None)
        inventer = request.GET.get('inventer', None)
        filing_date = request.GET.get('filing_date', None)
        applicant_name = request.GET.get('applicant_name', None)
        patent_number = request.GET.get('patent_number', None)
        relevancy_min = request.GET.get('relevancy_min', None)
        relevancy_max = request.GET.get('relevancy_max', None)

        # Create an empty query set
        queryset = Patent.objects.all()

        # Apply filters based on query parameters
        if id:
            queryset = queryset.filter(id=id)
        if source:
            queryset = queryset.filter(source__icontains=source)
        if date_published:
            queryset = queryset.filter(date_published=date_published)
        if pages_min and pages_max:
            queryset = queryset.filter(pages__range=(int(pages_min), int(pages_max)))
        elif pages_min:
            queryset = queryset.filter(pages__gte=int(pages_min))
        elif pages_max:
            queryset = queryset.filter(pages__lte=int(pages_max))
        if title:
            queryset = queryset.filter(title__icontains=title)
        if inventer:
            queryset = queryset.filter(inventer__icontains=inventer)
        if filing_date:
            queryset = queryset.filter(filing_date=filing_date)
        if applicant_name:
            queryset = queryset.filter(applicant_name__icontains=applicant_name)
        if patent_number:
            queryset = queryset.filter(patent_number__icontains=patent_number)
        if relevancy_min and relevancy_max:
            queryset = queryset.filter(relevancy__range=(float(relevancy_min), float(relevancy_max)))
        elif relevancy_min:
            queryset = queryset.filter(relevancy__gte=float(relevancy_min))
        elif relevancy_max:
            queryset = queryset.filter(relevancy__lte=float(relevancy_max))

        # Check if queryset is empty
        if not queryset.exists():
            return Response({"error": "No patents found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the filtered queryset
        serializer = PatentSerializer(queryset, many=True)

        # Cache the result for 10 minutes
        cache.set(cache_key, serializer.data, timeout=600)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "Invalid query parameters"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
