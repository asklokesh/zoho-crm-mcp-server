"""
Example: Using Zoho CRM MCP Server to manage leads.

This example demonstrates how to:
1. Initialize the Zoho CRM client
2. Fetch existing leads
3. Create a new lead
4. Search for specific leads
"""

import asyncio
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from zoho_crm_mcp import ZohoCRMClient, Config


async def main():
    """Main example function."""
    
    # Initialize configuration
    # Make sure to set environment variables or create a .env file
    config = Config()
    
    # Validate configuration
    try:
        config.validate_required_fields()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease set the following environment variables:")
        print("- ZOHO_CLIENT_ID")
        print("- ZOHO_CLIENT_SECRET")
        print("- ZOHO_REFRESH_TOKEN")
        return
    
    # Create client
    client = ZohoCRMClient(config)
    
    try:
        # Initialize client (this will refresh the access token)
        print("Initializing Zoho CRM client...")
        await client.initialize()
        print("✓ Client initialized successfully\n")
        
        # Example 1: Get leads
        print("=" * 50)
        print("Example 1: Fetching leads")
        print("=" * 50)
        try:
            leads_response = await client.get_leads(page=1, per_page=5)
            leads = leads_response.get('data', [])
            print(f"Found {len(leads)} leads:")
            for i, lead in enumerate(leads, 1):
                name = f"{lead.get('First_Name', '')} {lead.get('Last_Name', '')}".strip()
                email = lead.get('Email', 'N/A')
                company = lead.get('Company', 'N/A')
                print(f"  {i}. {name} - {email} ({company})")
        except Exception as e:
            print(f"Error fetching leads: {e}")
        
        # Example 2: Create a new lead
        print("\n" + "=" * 50)
        print("Example 2: Creating a new lead")
        print("=" * 50)
        try:
            new_lead_data = {
                "Last_Name": "Example",
                "First_Name": "Test",
                "Email": "test.example@demo.com",
                "Company": "Demo Company",
                "Phone": "+1-555-0123"
            }
            print(f"Creating lead: {new_lead_data['First_Name']} {new_lead_data['Last_Name']}")
            create_response = await client.create_lead(new_lead_data)
            
            if create_response.get('data'):
                lead_info = create_response['data'][0]
                if lead_info.get('status') == 'success':
                    print(f"✓ Lead created successfully!")
                    print(f"  Lead ID: {lead_info.get('details', {}).get('id', 'N/A')}")
                else:
                    print(f"✗ Lead creation failed: {lead_info.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"Error creating lead: {e}")
        
        # Example 3: Search for leads
        print("\n" + "=" * 50)
        print("Example 3: Searching for leads")
        print("=" * 50)
        try:
            search_criteria = "(Last_Name:equals:Example)"
            print(f"Search criteria: {search_criteria}")
            search_response = await client.search_records("Leads", search_criteria)
            results = search_response.get('data', [])
            print(f"Found {len(results)} matching leads:")
            for i, lead in enumerate(results, 1):
                name = f"{lead.get('First_Name', '')} {lead.get('Last_Name', '')}".strip()
                email = lead.get('Email', 'N/A')
                print(f"  {i}. {name} - {email}")
        except Exception as e:
            print(f"Error searching leads: {e}")
        
        # Example 4: Get contacts
        print("\n" + "=" * 50)
        print("Example 4: Fetching contacts")
        print("=" * 50)
        try:
            contacts_response = await client.get_contacts(page=1, per_page=3)
            contacts = contacts_response.get('data', [])
            print(f"Found {len(contacts)} contacts:")
            for i, contact in enumerate(contacts, 1):
                name = f"{contact.get('First_Name', '')} {contact.get('Last_Name', '')}".strip()
                email = contact.get('Email', 'N/A')
                print(f"  {i}. {name} - {email}")
        except Exception as e:
            print(f"Error fetching contacts: {e}")
        
        # Example 5: Get deals
        print("\n" + "=" * 50)
        print("Example 5: Fetching deals")
        print("=" * 50)
        try:
            deals_response = await client.get_deals(page=1, per_page=3)
            deals = deals_response.get('data', [])
            print(f"Found {len(deals)} deals:")
            for i, deal in enumerate(deals, 1):
                deal_name = deal.get('Deal_Name', 'N/A')
                amount = deal.get('Amount', 0)
                stage = deal.get('Stage', 'N/A')
                print(f"  {i}. {deal_name} - ${amount:,.2f} ({stage})")
        except Exception as e:
            print(f"Error fetching deals: {e}")
        
        print("\n" + "=" * 50)
        print("All examples completed!")
        print("=" * 50)
        
    finally:
        # Clean up
        await client.close()
        print("\n✓ Client closed")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
