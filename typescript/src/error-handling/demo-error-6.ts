/**
 * Async Exception Handling
 */

//1. We'll simulate an API request 
async function fetchUser(): Promise<string> {
    await new Promise(
        resolve => setTimeout(resolve, 1000)
    );
    throw new Error ("User service unavailable");
}

// 2. Call it with 'await'
async function main() {
    try {
        console.log("Calling API...");
        const user = await fetchUser();
        console.log("User:", user);
    } catch (error) {
        if (error instanceof Error) {
            console.log("API Call failed:", error.message);
        }
    }
}

main();

// If the Promise rejects, await turns that rejection into something you can handle using:
// try/catch

/**
Promise rejects
      ↓
await
      ↓
exception
      ↓
catch
 * 
 */