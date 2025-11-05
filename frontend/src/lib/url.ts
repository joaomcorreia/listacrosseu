export const API = "http://127.0.0.1:8000/api/v1";

export async function j(path: string) {
  try {
    const r = await fetch(`${API}${path}`, { cache: "no-store" });
    if (!r.ok) return null;
    return r.json();
  } catch (error) {
    console.error("API request failed:", error);
    return null;
  }
}