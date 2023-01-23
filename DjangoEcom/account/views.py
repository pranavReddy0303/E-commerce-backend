from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Category,Product,Cart,Cart_products,Order,Order_Item
from .serializers import RegistrationSerializer, CategorySerializer, ProductSerializer, UserSerializer, CartSerializer,SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserPasswordResetSerializer,Cart_productsSerializer,Order_ItemSerializer,OrderSerializer,MyTokenObtainPairSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import uuid
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView




class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        # serializer.is_valid(raise_exception = True)
        # serializer.save()
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                "RequestId": str(uuid.uuid4()),
                "Message": "User created successfully",
                
                "User": serializer.data}, status=status.HTTP_201_CREATED
                )
        
        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ListCategory(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DetailCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListProduct(generics.ListCreateAPIView):    
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserListProduct(generics.ListAPIView):    
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    


class DetailProduct(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserDetailProduct(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  


class ListUser(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)  
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListCart(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    

class DetailCart(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer   


class UserChangePasswordView(APIView):
  permission_classes = (permissions.IsAuthenticated,)
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


class UserlistCart(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class =  Cart_productsSerializer
    queryset = Cart_products.objects.all()


class UserdetailCart(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = Cart_productsSerializer
    queryset = Cart_products.objects.all()
    lookup_field = "cart_id"


class OrderDetail(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class =  OrderSerializer
    queryset = Order.objects.all()   

class OrderItem(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class =  Order_ItemSerializer
    queryset = Order_Item.objects.all()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer   



    
    
