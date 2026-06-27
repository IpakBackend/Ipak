from accounts.models import Account
from django.contrib.auth import authenticate
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.views import TokenRefreshView


from .schema.schemas import (  # account_token_refresh_schema,
    account_forgot_password_schema,
    account_login_schema,
    account_logout_schema,
    account_me_schema,
    account_signup_schema,
    account_forgot_password_verify_schema,
    account_password_reset_schema
)
from .serializers import (
    AccountChangePasswordSerializer,
    AccountForgotPasswordSerializer,
    AccountLoginSerializer,
    AccountLogoutSerializer,
    AccountSerializer,
    AccountTokenRefreshSerializer,
    AccountForgotPasswordVerifySerializer,
    AccountResetPasswordSerializer
)
from .services import AuthService, OTPService

# Create your views here.


@account_signup_schema
class AccountSignupView(APIView):
    serializer_class = AccountSerializer
    permission_classes = AllowAny,

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        account: Account = serializer.save()  # type:ignore
        data: dict[str, int | str | bool] = dict(AccountSerializer(account).data) | AuthService.issue_tokens(
            user=account,
            request=request._request
        )

        return Response(
            data=data,
            status=HTTP_201_CREATED
        )


@account_login_schema
class AccountLoginView(APIView):
    serializer_class = AccountLoginSerializer
    permission_classes = AllowAny,

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        account: Account = serializer.validated_data["user"]  # type:ignore

        return Response(data=AuthService.issue_tokens(
            user=account,
            request=request._request
        ), status=HTTP_200_OK)


@account_logout_schema
class AccountLogoutView(APIView):
    serializer_class = AccountLogoutSerializer
    permission_classes = IsAuthenticated,

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        sid: str | None = request.auth.get("sid")
        user_id: int = request.user.id

        if not sid:
            raise ValidationError(detail="Missing session id", code="required")

        refresh_token = AuthService.validate_refresh_token(
            refresh_token=serializer.validated_data[  # type:ignore
                "refresh_token"
            ],
            user_id=user_id,
            sid=sid
        )

        refresh_token.blacklist()

        AuthService.delete_session(sid=sid, user_id=user_id)

        return Response(status=HTTP_204_NO_CONTENT)


# @account_token_refresh_schema
class AccountTokenRefreshView(TokenRefreshView):
    serializer_class = AccountTokenRefreshSerializer


@account_me_schema
class AccountMeView(RetrieveAPIView):
    permission_classes = IsAuthenticated,
    queryset = Account.objects.filter(is_active=True)

    def get_object(self) -> Account:  # type:ignore
        return self.request.user  # type:ignore

    def get_serializer_class(self):  # type:ignore
        return AccountSerializer


class AccountChangePasswordView(APIView):
    permission_classes = IsAuthenticated,
    serializer_class = AccountChangePasswordSerializer

    def put(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict[str, str] = \
            serializer.validated_data  # type:ignore

        account = authenticate(
            request=request._request,
            username=request.user.username,
            password=validated_data["old_password"]
        )

        if not account:
            raise ValidationError(
                detail={"old_password": ["Wrong old password."]}, code="invalid"
            )

        sid: str | None = request.auth.get("sid")
        user_id: int = account.pk

        refresh_token = AuthService.validate_refresh_token(
            refresh_token=validated_data["refresh_token"],
            user_id=user_id,
            sid=sid
        )

        account.set_password(raw_password=validated_data["new_password"])
        account.save()

        refresh_token.blacklist()
        AuthService.invalidate_all_sessions(user_id=user_id)

        return Response(data=AuthService.issue_tokens(
            user=account,
            request=request._request
        ), status=HTTP_200_OK)


@account_forgot_password_schema
class AccountForgotPasswordView(APIView):
    serializer_class = AccountForgotPasswordSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]  # type:ignore
        account: Account | None = Account.objects.filter(
            email=email, is_active=True
        ).first()
        if not account:
            raise NotFound(
                detail={"email": ["Account with such email does not exist"]},
                code="not_found"
            )

        otp_code: str = OTPService.generate_otp(email=email)

        try:
            OTPService.send_otp_code(email=email, otp_code=otp_code)

            return Response({
                "email": email,
            })
        except Exception:
            OTPService.delete_otp(email=email)

            raise ValidationError(
                detail={"email": ["Failed to send email"]},
                code="invalid"
            )


@account_forgot_password_verify_schema
class AccountForgotPasswordVerifyView(APIView):
    serializer_class = AccountForgotPasswordVerifySerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email: str = serializer.validated_data["email"]  # type:ignore
        otp_code: str = serializer.validated_data["otp_code"]  # type:ignore

        account: Account | None = Account.objects.filter(
            email=email, is_active=True
        ).first()
        if not account:
            raise NotFound(
                detail={"email": ["Account with such email does not exist"]},
                code="not_found"
            )

        OTPService.check_otp(email=email, otp_code=otp_code)
        OTPService.delete_otp(email=email)

        return Response({
            "email": email,
            "reset_token": OTPService.generate_reset_token(email=email)
        })


@account_password_reset_schema
class AccountResetPasswordView(APIView):
    serializer_class = AccountResetPasswordSerializer

    def patch(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token: str = serializer.validated_data["token"]  # type:ignore
        email: bytes | None = OTPService.get_email_by_reset_token(token=token)

        if not email:
            raise ValidationError(
                detail={"token": ["Invalid reset token."]},
                code="invalid"
            )

        account: Account | None = Account.objects.filter(
            email=email.decode(), is_active=True
        ).first()

        if not account:
            raise NotFound(
                detail="Account with such email does not exist",
                code="not_found"
            )

        password: str = serializer.validated_data["password"]  # type:ignore
        account.set_password(raw_password=password)
        account.save()

        AuthService.invalidate_all_sessions(user_id=account.id)

        return Response(data=AuthService.issue_tokens(
            user=account,
            request=request._request
        ), status=HTTP_200_OK)
