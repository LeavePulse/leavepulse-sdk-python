"""LeavePulse SDK — OAuth2 authorization-code + PKCE facade for 3rd-party web
apps acting on behalf of a LeavePulse *user*.

:func:`build_authorize_url` is a pure helper: it mints a PKCE S256 pair and
assembles the authorize URL. The app sends the user to that URL; a **frontend**
page renders the visual consent (the SDK never drives a browser). After the
redirect-back with ``?code=``, :func:`exchange_code` trades the code for tokens
at ``/auth/oauth/token`` (form-urlencoded) and returns an auto-refreshing
:class:`~leavepulse_sdk.credentials.OAuth2Credential`. The exchange is driven
through the caller's transport, so it works without the generated
``auth.oauth2.*`` methods existing yet.
"""

from __future__ import annotations

import base64
import hashlib
import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

from .credentials import OAuth2Credential, TokenPair
from .transport import Transport

#: Where the OAuth2 token exchange is performed (NOTE: ``/auth/oauth/token``).
_TOKEN_PATH = "/auth/oauth/token"


@dataclass(frozen=True)
class AuthorizeUrl:
    """Result of :func:`build_authorize_url`: the URL to send the user to, plus
    the PKCE verifier and state the app must keep until :func:`exchange_code`."""

    #: The authorize URL to open in the frontend (visual consent).
    url: str
    #: PKCE ``code_verifier`` — keep secret, pass back to ``exchange_code``.
    code_verifier: str
    #: The ``state`` echoed back on redirect — verify it matches.
    state: str


def build_authorize_url(
    *,
    client_id: str,
    redirect_uri: str,
    scope: list[str],
    authorize_base_url: str,
    state: str | None = None,
) -> AuthorizeUrl:
    """Build an OAuth2 authorize URL with a fresh PKCE (S256) challenge.

    Pure (no network). ``response_type=code``, ``code_challenge_method=S256``.

    :param client_id:           OAuth2 client id of the third-party app.
    :param redirect_uri:        redirect URI registered for the app.
    :param scope:               requested scopes; joined with spaces per OAuth2.
    :param authorize_base_url:  base URL of the authorize page (a frontend URL).
    :param state:               CSRF/anti-forgery state; random when omitted.
    """
    code_verifier = _random_url_safe(64)
    resolved_state = state if state is not None else _random_url_safe(32)
    code_challenge = _s256_challenge(code_verifier)

    params = urlencode(
        {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(scope),
            "state": resolved_state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
    )
    base = authorize_base_url.rstrip("/")
    return AuthorizeUrl(
        url=f"{base}?{params}",
        code_verifier=code_verifier,
        state=resolved_state,
    )


@dataclass(frozen=True)
class _TokenExchangeResponse:
    """``/auth/oauth/token`` response shape (wire snake_case)."""

    access_token: str
    refresh_token: str | None = None
    expires_in: float | None = None
    token_type: str | None = None


async def exchange_code(
    transport: Transport,
    *,
    client_id: str,
    code: str,
    redirect_uri: str,
    code_verifier: str,
) -> OAuth2Credential:
    """Exchange an authorization code for tokens at ``/auth/oauth/token``
    (form-urlencoded, ``grant_type=authorization_code``) and return an
    auto-refreshing :class:`~leavepulse_sdk.credentials.OAuth2Credential`.

    Driven through the supplied ``transport`` (channel ``auth``), so it does not
    depend on generated code.
    """
    tokens = await _post_token(
        transport,
        {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
        },
    )

    async def refresh(refresh_token: str) -> TokenPair:
        # Auto-refresh via the same /token endpoint (refresh_token grant).
        pair = await _post_token(
            transport,
            {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
            },
        )
        return TokenPair(
            access_token=pair.access_token,
            refresh_token=pair.refresh_token,
            expires_in=pair.expires_in,
        )

    return OAuth2Credential(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token or "",
        refresh_fn=refresh,
        expires_in=tokens.expires_in,
    )


async def _post_token(
    transport: Transport, form: dict[str, str]
) -> _TokenExchangeResponse:
    """POST a form-encoded grant request to ``/auth/oauth/token`` (auth channel)."""
    raw = await transport.request(
        "POST", _TOKEN_PATH, channel="auth", form=form
    )
    data = raw if isinstance(raw, dict) else {}
    return _TokenExchangeResponse(
        access_token=str(data.get("access_token", "")),
        refresh_token=data.get("refresh_token"),
        expires_in=data.get("expires_in"),
        token_type=data.get("token_type"),
    )


def _base64_url_encode(data: bytes) -> str:
    """Base64url-encode bytes (no padding), per RFC 7636."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _random_url_safe(byte_length: int) -> str:
    """A cryptographically-random URL-safe string of ``byte_length`` entropy."""
    return _base64_url_encode(secrets.token_bytes(byte_length))


def _s256_challenge(verifier: str) -> str:
    """Compute the PKCE S256 ``code_challenge`` from a verifier."""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return _base64_url_encode(digest)
