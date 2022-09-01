## Use Case
Assessing risk or criticality typically requires manual input from experts and rarely benefits from past occurrences. This makes the overall process time consuming and does not necessarily yield consistency over time. To digitize this part of the process, we propose a machine learning service for criticality assessments in this mission. The criticality assessments in this mission is exemplary and based on restaurant inspections where a health inspector, the expert, screens a restaurant and writes down violations that then lead to a score of this restaurant. The provided data of the mission is based on a  publicly available dataset (Restaurant Scores - LIVES Standard in San Francisco published by Public Health) which has been restructured to fit the machine learning approach of multi output regression. Since multi output regression is not provided by SAP Data Attribute Recommendation service (DAR), this mission showcases a solution with the help of SAP AI Core. The approach of this mission can be easily adapted to other similar situations of criticality assessments.
 
This mission is based on a real customer use case about criticality assessments which is currently in productization.

## Current Position - What is the challenge?
Organizations can have complex rules for their criticality assessments. Many times, the assessment is dominated by manual input, which is prone to errors, can be time consuming. Besides that, due to individual approaches of different processors, inconsistencies can arise over the time, yielding different results for similar input.

## Destination - What is the outcome?
The solution uses machine learning to assist the processor of criticality assessments by translating descriptions and details of a criticality assessment to multiple scores necessary to conclude the assessment.

## How You Get There - What is the solution?
A machine learning service leveraging the capabilities of SAP Business Technology Platform (SAP AI Core and SAP AI Launchpad) to assess the descriptions of a criticality assessment (in this case, the violations of a restaurant inspection). These descriptions are represented by unstructured text which will be transformed to vectors to finally perform a parallel regression for determining multiple scores.