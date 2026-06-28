from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.response import Response

from .models import ReturnRequest
from .serializers import ReturnRequestSerializer


class ReturnRequestViewSet(viewsets.ModelViewSet):

    serializer_class = ReturnRequestSerializer
    permission_classes = [IsAuthenticated]

    queryset = ReturnRequest.objects.all().order_by(
        "-created_at"
    )

    def get_queryset(self):

        user = self.request.user

        return ReturnRequest.objects.filter(
            customer=user
        ).order_by("-created_at")

    def perform_create(self, serializer):

        serializer.save(
            customer=self.request.user
        )


# ===========================
# VENDOR RETURN REQUESTS
# ===========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_return_requests(request):

    vendor = request.user

    if not vendor.is_vendor:
        return Response(
            {"error": "Only vendors can access this"},
            status=403
        )

    returns = ReturnRequest.objects.filter(
        order__product__vendor=vendor
    ).order_by("-created_at")

    serializer = ReturnRequestSerializer(
        returns,
        many=True
    )

    return Response(serializer.data)


# ===========================
# UPDATE RETURN STATUS
# ===========================

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_return_status(request, pk):

    vendor = request.user

    if not vendor.is_vendor:
        return Response(
            {"error": "Only vendors can update returns"},
            status=403
        )

    try:

        return_request = ReturnRequest.objects.get(
            id=pk,
            order__product__vendor=vendor
        )

    except ReturnRequest.DoesNotExist:

        return Response(
            {"error": "Return request not found"},
            status=404
        )

    status_value = request.data.get("status")

    allowed = [
        "approved",
        "rejected",
        "refunded"
    ]

    if status_value not in allowed:

        return Response(
            {"error": "Invalid status"},
            status=400
        )

    return_request.status = status_value
    return_request.save()

    return Response({
        "message":
            "Return status updated successfully",
        "status": return_request.status
    })