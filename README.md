# Azure Cost Optimization: Archiving Old Cosmos DB Records

## Problem Statement
The Cosmos DB storing billing records is growing too large. Most records >3 months old are rarely accessed. We need to reduce costs while keeping old data accessible.

## Solution Summary
We use a tiered storage approach:

-  Hot data (< 3 months): stored in Cosmos DB
-  Cold data (> 3 months): archived to Azure Blob Storage (Cool tier)
- Existing APIs will read from Cosmos DB first, then fallback to Blob if needed

## Architecture

![Architecture Diagram](./diagrams/architecture.png)

## Components
- **Azure Function** (`archive-function/main.py`) – moves data from Cosmos DB to Blob
- **Backend Logic** (`backend/read_with_fallback.py`) – fallback logic to serve archived records

## Deployment Steps

1. Deploy the Azure Function (Timer Trigger) with access to Cosmos and Blob
2. Integrate `read_with_fallback.py` into your backend API
3. Monitor logs & storage costs

## Benefits
- ~80% cost savings on storage
- Zero downtime
- No API changes
- Fully serverless and scalable

## ✨ Points
- Architecture Diagram
- Code included
