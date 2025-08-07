from crewai import Agent, Task, Crew
from prod_input import get_structured_input

def generate_queries():
    input_data = get_structured_input()

    search_query_agent = Agent(
        role="Market Research Analyst",
        goal="Generate intelligent and specific search queries",
        backstory="Expert at generating queries for competitive and market research.",
        allow_delegation=False,
    )

    task = Task(
        description=f"""
You are a skilled Market Research Analyst tasked with helping generate a market report for a new product.

Your job is to craft **10 high-quality Google search queries** to gather data for the following report sections:
1. Market Context
2. Market Size
3. Market Segmentation
4. Target Customers

### Input:
- **Product Name:** {input_data['product_name']}
- **Description:** {input_data['product_description']}
- **Features:** {input_data['product_features']}
- **Pricing:** {input_data['pricing']}
- **Target Demographics:** {input_data['demographics']}

### Instructions for Queries:
- Generate 2–3 queries for each of the four report sections above.
- Each query should be specific and reflect the input context (e.g., product type, audience, geography, pricing, or niche).
- Include keywords like "2024", "report", "industry trends", "growth", "market analysis", "customer persona", "segmentation", etc.
- If location is mentioned in demographics, include it in queries (e.g., "India", "North America").
- Avoid generic or vague queries like “What is a CRM?” or “Benefits of technology.”

### Output Format:
Return a numbered list of 10 clear, specific, Google search queries.
""",
        expected_output="10 concise and specific Google search queries related to the product's market analysis.",
        agent=search_query_agent
    )

    crew = Crew(
        agents=[search_query_agent],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()

