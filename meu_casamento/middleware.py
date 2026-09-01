import time
import logging
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Extract the client IP from request headers.
    Supports Cloud Run and reverse proxies (X-Forwarded-For / X-Real-IP),
    falling back to REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR', 'unknown')


class PermissionsPolicyMiddleware:
    """
    Middleware to attach the Permissions-Policy HTTP header to responses.
    Controls which browser features and APIs are enabled or restricted.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        policy_header = self.get_permissions_policy_header()
        if policy_header and "Permissions-Policy" not in response:
            response["Permissions-Policy"] = policy_header
        return response

    def get_permissions_policy_header(self):
        policy = getattr(settings, "PERMISSIONS_POLICY", None)
        if not policy:
            return None

        if isinstance(policy, str):
            return policy

        directives = []
        for feature, allowlist in policy.items():
            if isinstance(allowlist, str):
                allowlist = [allowlist]

            if not allowlist:
                directives.append(f"{feature}=()")
            elif "*" in allowlist:
                directives.append(f"{feature}=*")
            else:
                formatted_values = []
                for val in allowlist:
                    if val in ("self", "'self'"):
                        formatted_values.append("self")
                    elif val in ("none", "'none'", "()"):
                        formatted_values = []
                        break
                    else:
                        clean_val = val.strip("'\"")
                        formatted_values.append(f'"{clean_val}"')

                if formatted_values:
                    directives.append(f"{feature}=({' '.join(formatted_values)})")
                else:
                    directives.append(f"{feature}=()")

        return ", ".join(directives)


class AdminLoginRateLimitMiddleware:
    """
    Middleware to rate limit POST requests to the Django admin login endpoint,
    preventing automated brute-force attacks and credential stuffing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and self.is_admin_login(request):
            if not self.check_rate_limit(request):
                logger.warning(f"Admin login rate limit exceeded for IP {get_client_ip(request)}")
                return HttpResponse(
                    "Muitas tentativas de login. Por favor, aguarde alguns minutos antes de tentar novamente.",
                    status=429,
                    content_type="text/plain; charset=utf-8",
                )
        return self.get_response(request)

    def is_admin_login(self, request):
        try:
            from django.urls import reverse
            login_url = reverse('admin:login')
            return request.path == login_url or request.path == login_url.rstrip('/')
        except Exception:
            return request.path.rstrip('/').endswith('/login')

    def check_rate_limit(self, request):
        max_attempts = getattr(settings, "ADMIN_LOGIN_RATE_LIMIT_MAX_ATTEMPTS", 5)
        window = getattr(settings, "ADMIN_LOGIN_RATE_LIMIT_WINDOW", 300)

        ip = get_client_ip(request)
        cache_key = f"admin_login_ratelimit_{ip}"
        requests = cache.get(cache_key, [])
        now = time.time()

        requests = [req_time for req_time in requests if now - req_time < window]

        if len(requests) >= max_attempts:
            return False

        requests.append(now)
        cache.set(cache_key, requests, window)
        return True


