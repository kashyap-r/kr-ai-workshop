
// create a new object type
type InvestmentData = {
    initialAmount: number;
    annualContribution: number;
    expectedReturn: number;
    duration: number;
};

type InvestmentResult = {
    year: string;
    totalAmount: number;
    totalContributions: number;
    totalIntrestEarned: number;
};

type calculationResult = InvestmentResult[] | string;

function calculateInvestment(data: InvestmentData): calculationResult {
    const { initialAmount, annualContribution, expectedReturn, duration } = data;

    if (initialAmount < 0) {
        return "Initial investment amount must be be at least zero!";
    }

    if (duration <= 0){
        return "Duration provided is invalid!"
    }

    if (expectedReturn < 0){
        return "expected return must be at least zero"
    }

    let total = initialAmount;
    let totalContributions = 0;
    let totalIntrestEarned = 0; 

    const annualResults: InvestmentResult[] = [];

    for (let i=0; i<duration; i++) {
        total = total * ( 1 + expectedReturn);
        totalIntrestEarned = total - totalContributions - initialAmount;
        totalContributions = totalContributions + annualContribution;
        total = total + annualContribution;

        annualResults.push({
            year: `Year ${i+1}`,
            totalAmount: total,
            totalIntrestEarned,
            totalContributions
        });
    }
    return annualResults;
}

function printResults(results: calculationResult) {
    if (typeof results == 'string'){
        console.log(results);
        return;
    }

    for (const yearEndResult of results){
        console.log(yearEndResult.year);
        console.log(`Total: ${yearEndResult.totalAmount.toFixed()}`);
        console.log(`Total Contributions: ${yearEndResult.totalContributions.toFixed()}`);
        console.log(`Total Interest Earned: ${yearEndResult.totalIntrestEarned.toFixed()}`);
        console.log("---------------------------------------")
        console.log()
    }
}

const investmentData: InvestmentData = {
    initialAmount: 5000, 
    annualContribution: 500,
    expectedReturn: 0.08,
    duration: 10
};

const results = calculateInvestment(investmentData);
printResults(results);
