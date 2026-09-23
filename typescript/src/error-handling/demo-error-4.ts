/**
 * Custom Error Classes 
 * 
 */
// Imagine the application retrieves documents 

class DocumentNotFoundError extends Error {
    constructor(public documentID: string) {
        super(`Document ${documentID} was not found`);
        this.name = "DocumentNotFoundError";
    }
}

function getDocument(documentID: string): string {
    const documents: Record<string, string> = {
        "DOC-001": "Parental Leave Policy",
        "DOC-002": "Travel Policy"
    };
    const document = documents[documentID];

    if (!document) {
        throw new DocumentNotFoundError(documentID);
    }
    return document;
}

try {
    // throw 500;
    const document = getDocument("DOC-999");
    console.log(document);

} catch(error) {
    if (error instanceof DocumentNotFoundError) {
        console.log("Document lookup failed.");
        console.log("Document ID:", error.documentID);
        console.log("Message:", error.message);
    }
    else {
        console.log("Kashyap induced an Error!", error);
    }
}