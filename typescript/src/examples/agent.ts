class Agent{
    name: string;
    model: string;

    constructor(name: string, model: string){
        this.name = name;
        this.model = model;
    }

    run (task: string): string {
        return `${this.name} is executing: ${task}`;
    }
}

const researchAgent = new Agent("ResearchAgent", "gpt-5");

console.log(researchAgent.run("Find parental leave policy"));
