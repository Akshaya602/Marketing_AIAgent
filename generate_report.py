import json
from crewai import Agent, Task, Crew
from prod_input import get_structured_input

def generate_report():
    with open("scraped_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    product_info = get_structured_input()
    product_name = product_info["product_name"]
    product_description = product_info["product_description"]
    demographics = product_info["demographics"]

    sections = ["Market Context", "Market Size", "Market Segmentation", "Target Customers"]

    #agent
    report_writer = Agent(
        role="Market Analyst and Report Writer",
        goal="Write a detailed market research report on a specific product using structured inputs and scraped data.",
        backstory="Specialist in generating structured reports from web data and citing sources accurately.",
        allow_delegation=False,
    )

    final_report = {}

    for section in sections:
        section_content = "\n\n".join(
            [
                item['content'] + f"\n(Source: {item['url']})"
                for query, items in data.items()
                for item in items
                if section.lower() in query.lower()
            ]
        )[:8000]

        task = Task(
            description=f"""You are writing the **{section}** section of a market research report for the product: **{product_name}**.

### Product Description:
{product_description}

### Target Demographics:
{demographics}

### Your Task:
Use ONLY the provided web-scraped data relevant to this section.
Avoid generalizations—your insights must be directly relevant to this product and its market.
Cite sources inline and make the content structured, insightful, and professional.

### Data:
{section_content}
""",
            expected_output=f"A well-written section on {section.lower()} with insights and inline citations.",
            agent=report_writer
        )

        crew = Crew(agents=[report_writer], tasks=[task])
        result = crew.kickoff()
        final_report[section] = result

    return final_report
