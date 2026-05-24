import type { NextRequest } from "next/server";

const INTERNAL_AUTH_HEADER_NAME = "X-DeerFlow-Internal-Token";

function normalizeBaseUrl(raw: string | undefined) {
  const value = raw?.trim();
  if (!value) {
    return "http://127.0.0.1:8001";
  }
  const withScheme = /^https?:\/\//i.test(value) ? value : `https://${value}`;
  return withScheme.replace(/\/+$/, "");
}

const GATEWAY_BASE_URL = normalizeBaseUrl(
  process.env.DEER_FLOW_INTERNAL_GATEWAY_BASE_URL ??
    process.env.RAILWAY_SERVICE_EVIDARAOS_GATEWAY_URL,
);

function buildGatewayUrl(path: string[], request: NextRequest) {
  const suffix = path.length ? `/${path.join("/")}` : "";
  const url = new URL(`/api${suffix}`, GATEWAY_BASE_URL);
  url.search = request.nextUrl.search;
  return url;
}

async function proxyLangGraphRequest(
  request: NextRequest,
  context: { params: Promise<{ path?: string[] }> },
) {
  const { path = [] } = await context.params;
  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("connection");
  headers.delete("content-length");

  const internalToken = process.env.DEER_FLOW_INTERNAL_AUTH_TOKEN?.trim();
  if (internalToken) {
    headers.set(INTERNAL_AUTH_HEADER_NAME, internalToken);
  }

  const hasBody = !["GET", "HEAD"].includes(request.method);
  const response = await fetch(buildGatewayUrl(path, request), {
    method: request.method,
    headers,
    body: hasBody ? await request.arrayBuffer() : undefined,
    redirect: "manual",
  });

  return new Response(await response.arrayBuffer(), {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
}

export async function GET(
  request: NextRequest,
  context: { params: Promise<{ path?: string[] }> },
) {
  return proxyLangGraphRequest(request, context);
}

export async function POST(
  request: NextRequest,
  context: { params: Promise<{ path?: string[] }> },
) {
  return proxyLangGraphRequest(request, context);
}

export async function PUT(
  request: NextRequest,
  context: { params: Promise<{ path?: string[] }> },
) {
  return proxyLangGraphRequest(request, context);
}

export async function PATCH(
  request: NextRequest,
  context: { params: Promise<{ path?: string[] }> },
) {
  return proxyLangGraphRequest(request, context);
}

export async function DELETE(
  request: NextRequest,
  context: { params: Promise<{ path?: string[] }> },
) {
  return proxyLangGraphRequest(request, context);
}
