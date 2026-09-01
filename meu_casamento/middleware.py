from django.conf import settings


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

