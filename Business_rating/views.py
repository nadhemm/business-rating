import coreapi
import coreschema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

from Business_rating.functions import is_valid_business, get_categories
from Business_rating.models import Business, Review


class SearchAPI(APIView):
    def get(self, request):
        q = request.GET.get('q')
        if not q:
            return Response({'success': False, 'Error': 'Wrong format'}, status=status.HTTP_400_BAD_REQUEST)
        businesses = Business.objects.filter(name__contains=q)
        res = [(business.name, business.id, business.logo.path) for business in businesses]
        return Response({'success': True, 'results': res}, status=status.HTTP_200_OK)

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field("q", True, description="query string for search"),
        ]
    )


class BusinessDetailsAPI(APIView):
    def get(self, request):
        business_id = request.GET.get('business_id')
        business_details = Business.objects.get(id=business_id)
        result = {'name': business_details.name,
                  'address': business_details.address,
                  'phone_number': business_details.phone_number,
                  'category': business_details.category,
                  'logo': business_details.logo.path,
                  'reviews': business_details.get_reviews()
                  }
        return Response({'success': True, 'results': result}, status=status.HTTP_200_OK)

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field("business_id", True, description="1-indexed DB id"),
        ]
    )


class AddBusinessAPI(APIView):
    def post(self, request):
        """
           This one is for adding a business
           """
        name = request.data.get('name')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number')
        category = request.data.get('category')
        check = is_valid_business(name=name, category=category)
        if not check['success']:
            print("Bad request", check['message'])
            return Response({'Error': check['message']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Business.objects.create(name=name, address=address, phone_number=phone_number, category=category)
            return Response({'success': True, 'message': 'Business successfully created'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print("An error occurred while creating the business", e)
            return Response({'success': False, 'error': "An error occurred while creating the business"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field("name", True, description="ex: 'Barreka'", example="barreka"),
            coreapi.Field("address", False, description="ex: 'Centre urbain nord'", schema=coreschema.String()),
            coreapi.Field("phone_number", False, description="ex: '21012345'"),
            coreapi.Field("category", False, description="Must be one of these " + str(get_categories())),
        ]
    )


class ReviewBusinessAPI(APIView):
    def post(self, request):
        business_id = request.data.get('business_id')
        stars = request.data.get('stars')
        comment = request.data.get('comment')
        reviewer = request.data.get('reviewer_name')
        try:
            business = Business.objects.get(id=business_id)
        except Exception as e:
            return Response({'Error': 'Could not retrieve Business with id ' + business_id + ' ' + str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        Review.objects.create(stars=stars, comment=comment, business=business, reviewer=reviewer)
        return Response({'success': True, 'message': 'Review successfully created'},
                        status=status.HTTP_201_CREATED)

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field("business_id", True, description="1-indexed DB id"),
            coreapi.Field("stars", True, description="a number from 1 to 5"),
            coreapi.Field("comment", False, description="ex: 'Amazing place'"),
            coreapi.Field("reviewer_name", False, description="Name of the reviewer"),
        ]
    )
