import { API_BASE_URL } from "./routes";

export { API_BASE_URL, API_ROUTES } from "./routes";

export interface ListParams {
  page?: number;
  page_size?: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
  search?: string;
  status?: string;
  severity?: string;
  hours?: number;
  [key: string]: string | number | undefined;
}

const DEFAULT_TIMEOUT_MS = 15_000;

export interface FetchApiOptions extends RequestInit {
  timeoutMs?: number;
}

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status?: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function buildQuery(params?: ListParams): string {
  if (!params) return "";
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null) {
      query.set(key, String(value));
    }
  }
  const serialized = query.toString();
  return serialized ? `?${serialized}` : "";
}

export async function fetchApi<T>(
  path: string,
  init?: FetchApiOptions,
): Promise<T> {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, ...requestInit } = init ?? {};
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(path, {
      ...requestInit,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...requestInit.headers,
      },
    });

    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      const message =
        (body as { error?: string; detail?: string }).error ??
        (body as { detail?: string }).detail ??
        `API request failed (${response.status})`;
      throw new ApiError(message, response.status);
    }

    return response.json() as Promise<T>;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError(`Request timed out after ${timeoutMs}ms`, 408);
    }
    throw new ApiError(
      error instanceof Error ? error.message : "Network request failed",
    );
  } finally {
    clearTimeout(timeoutId);
  }
}

export async function fetchList<T>(
  path: string,
  params?: ListParams,
  init?: FetchApiOptions,
): Promise<import("@/types/api").PaginatedResponse<T>> {
  return fetchApi(`${path}${buildQuery(params)}`, init);
}
