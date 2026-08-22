export function logEvent(
  event: string,
  data: Record<string, unknown>
) {

  console.log(
    JSON.stringify({
      timestamp: new Date().toISOString(),
      event,
      ...data
    })
  );
}

