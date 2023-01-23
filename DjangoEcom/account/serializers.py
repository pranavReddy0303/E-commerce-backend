from rest_framework import serializers
from .models import Category, Product, Cart, Cart_products,Order,Order_Item
from django.contrib.auth.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)

        if not first_name.isalpha():
            raise serializers.ValidationError({'firstname': ('enter a valid first_name')})

        if not last_name.isalpha():
            raise serializers.ValidationError({'lastname': ('enter a valid last_name')})    

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('username already exists')})

        return super().validate(args)
  

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = (
            'id',
            'title'
        )
        model = Category 




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'product_tag',
            'name',
            'category',
            'stock_quantity',
            'price',
            
        )
        model = Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'username',
            'email',
            
        )


class CartSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    

    class Meta:
        model = Cart
        fields = ('id','user', 'created_at')


class Cart_productsSerializer(serializers.ModelSerializer):

    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    Total_price= serializers.SerializerMethodField(method_name="total_price")
    
    
    class Meta:
        model = Cart_products
        fields = ('cart_id', 'created_at', 'product_id','quantity','Total_price') 

    def total_price(self, cartitem:Cart_products):
        return cartitem.quantity * cartitem.product_id.price        

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      # Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')    


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user_id',
            'is_paid'
        ]
class Order_ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Item
        fields = [
            'order_id',
            'product_id',
            'total_amount'
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        print(user.username,'user.username')
        token['username'] = user.username
        print('token1',token['username'])
        # user=user.username
        # ...
        print(user.is_staff,'user.is_staff')
        if user.is_staff == False:
            carts = Cart.objects.filter(user=user, is_active=True)
           
            if not carts:
              Cart.objects.create(user=user, is_active=True)
        return token



        







