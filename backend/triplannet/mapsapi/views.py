import json
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import AutoComplete, Query, Place

class PlaceAutoComplete(APIView):
    def _check_query_cache(self, query):
        if Query.objects.filter(query=query).exists():
            return True
        else:
            return False

    def parse(self, data, query):
        if not isinstance(data, dict) or "predictions" not in data:
            return None
        predictions = data["predictions"]
        parse_data = []
        for idx, prediction in enumerate(predictions):
            parse_data.append({
                "search_index": idx,
                "query": query,
                "description": prediction.get("description", None),
                "structured_formatting": prediction.get("structured_formatting", {}),
                "place_id": prediction.get("place_id", None),
            })
        return parse_data

    def cache(self, data, query):
        new_query = Query.objects.create(query=query)
        tuples = []
        for row in data:
            autoComplete = AutoComplete()
            autoComplete.search_index = row.get("search_index")
            autoComplete.query = new_query
            autoComplete.description = row.get("description")
            autoComplete.structured_formatting = json.dumps(row.get("structured_formatting"))
            autoComplete.place_id = row.get("place_id")
            tuples.append(autoComplete)
        AutoComplete.objects.bulk_create(tuples)

    def get(self, request, query, *args, **kwargs):
        if self._check_query_cache(query):
            print("[CACHED] {}".format(query))
            query_item = Query.objects.get(query=query)
            completes = AutoComplete.objects.filter(query=query_item)
            completes = [{"search_index": complete.search_index,
                       "query": complete.query.query,
                       "description": complete.description,
                       "structured_formatting": json.loads(complete.structured_formatting or '{}'),
                       "place_id": complete.place_id} for complete in completes]
            return Response(completes, status=status.HTTP_200_OK)
        else:
            url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
            params = {
                "input": query,
                "key": getattr(settings, 'CREDENTIAL_GOOGLE_MAPS', 'KEY')
            }
            response = requests.get(url, params=params)
            if response.status_code != 200:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data = response.json()
            completes = self.parse(data, query)
            if completes == None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.cache(completes, query)
            return Response(completes, status=status.HTTP_201_CREATED)



class PlaceSearch(APIView):
    r"""
    Search Places given query

    ** currently not used **
    """

    def _check_query_cache(self, query):
        if Query.objects.filter(query=query).exists():
            return True
        else:
            return False

    def parse(self, data, query):
        if not isinstance(data, dict) or "results" not in data:
            return None
        results = data["results"]
        parse_data = []
        for idx, result in enumerate(results):
            photos = result.get("photos", [])
            photo = photos[0] if photos else {}
            parse_data.append({
                "search_index": idx,
                "query": query,
                "name": result.get("name", None),
                "formatted_address": result.get("formatted_address", None),
                "lat": result.get("geometry", {}).get("location", {}).get("lat", 0.0),
                "lng": result.get("geometry", {}).get("location", {}).get("lng", 0.0),
                "place_id": result.get("place_id", None),
                "types": (result.get("types", []) or [None])[0],
                "rating": result.get("rating", None),
                "icon": result.get("icon", None),
                "photo_reference": photo.get("photo_reference", None),
                "photo_width": photo.get("width", None),
                "photo_height": photo.get("height", None),
            })
        return parse_data

    def cache(self, data, query):
        new_query = Query.objects.create(query=query)
        tuples = []
        for row in data:
            place = Place()
            place.search_index = row.get("search_index")
            place.query = new_query
            place.name = row.get("name")
            place.formatted_address = row.get("formatted_address")
            place.lat = row.get("lat")
            place.lng = row.get("lng")
            place.place_id = row.get("place_id")
            place.types = row.get("types")
            place.rating = row.get("rating")
            place.icon = row.get("icon")
            place.photo_reference = row.get("photo_reference")
            place.photo_width = row.get("photo_width")
            place.photo_height = row.get("photo_height")
            tuples.append(place)
        Place.objects.bulk_create(tuples)

    def get(self, request, query, *args, **kwargs):
        if self._check_query_cache(query):
            print("[CACHED] {}".format(query))
            query_item = Query.objects.get(query=query)
            places = Place.objects.filter(query=query_item)
            places = [{"search_index": place.search_index,
                       "query": place.query.query,
                       "name": place.name,
                       "formatted_address": place.formatted_address,
                       "lat": place.lat,
                       "lng": place.lng,
                       "place_id": place.place_id,
                       "types": place.types,
                       "rating": place.rating,
                       "icon": place.icon,
                       "photo_reference": place.photo_reference,
                       "photo_width": place.photo_width,
                       "photo_height": place.photo_height} for place in places]
            return Response(places, status=status.HTTP_200_OK)
        else:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                "query": query,
                "key": getattr(settings, 'CREDENTIAL_GOOGLE_MAPS', 'KEY')
            }
            response = requests.get(url, params=params)
            if response.status_code != 200:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data = response.json()
            places = self.parse(data, query)
            if places == None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.cache(places, query)
            return Response(places, status=status.HTTP_201_CREATED)

