from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response


def request_get_or_none(request, key):
    value = request.data.get(key, None)
    if value is None:
        return None
    else:
        return value


def request_get_query_or_none(request, key):
    value = request.GET.get(key, None)
    if value is None:
        return None
    else:
        return value


def raise_required_key(key):
    return Response(
        status=status.HTTP_400_BAD_REQUEST, data={key: "this key is required."}
    )


def raise_validation_error(key):
    raise serializers.ValidationError({key: "This field is required."})
