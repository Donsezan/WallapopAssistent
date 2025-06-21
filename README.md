# Wallapop Item Monitor

This Python application allows users to monitor items on Wallapop, a popular online marketplace. It provides features for advanced searching, filtering, and real-time notifications for new items matching user-defined criteria.

## Main Features

*   **Multiple Search Monitoring:**
    *   Define and manage several distinct search queries simultaneously.
    *   Each search has its own configuration for keywords and filters.
    *   Content for each search is fetched and stored independently.

*   **Advanced Search & Filtering:**
    *   **Keyword Search:** Search for items using specific keywords. Multiple keywords can be combined.
    *   **Description Filtering:** Extend your search to include the item's description, not just the title.
    *   **Price Range Filtering:** Specify minimum and maximum price limits to narrow down results.

*   **Automated Content Fetching:**
    *   Interacts directly with the Wallapop API to retrieve the latest item listings.
    *   Handles pagination to gather comprehensive results.

*   **Local Caching & Offline Capability:**
    *   Search parameters and fetched item data (including images) are stored locally.
    *   Allows browsing of previously fetched items even when offline or if the API is temporarily unavailable.
    *   Efficiently updates local cache with only new or changed items.

*   **Desktop Toast Notifications:**
    *   Receive instant desktop notifications (Windows Toasts) when new items matching your criteria are found.
    *   Notifications include item title, image, and a direct link to the Wallapop listing.

*   **Tabbed User Interface:**
    *   A user-friendly interface (built with CustomTkinter) organizes different searches into tabs.
    *   Easily switch between searches and view their respective items.
    *   Displays items with their image, title, and price.

## Overview

The application works by:

1.  Allowing users to configure one or more search profiles, specifying keywords and filter options (description content, price range).
2.  Periodically querying the Wallapop API for items matching these profiles.
3.  Comparing fetched results against a local history of items already seen.
4.  Storing new items and their images locally.
5.  Alerting the user to new items via desktop notifications.
6.  Displaying all monitored items in a tabbed interface, allowing users to click through to the Wallapop website.

## Key Technologies

*   **Python:** Core programming language.
*   **CustomTkinter:** For the graphical user interface.
*   **Requests:** For making HTTP requests to the Wallapop API.
*   **Windows-Toasts:** For displaying desktop notifications on Windows.
*   **Pillow (PIL):** For image processing.

## Running the Application (General Steps)

(Detailed setup instructions would depend on the final packaging and dependencies)

1.  **Ensure Python is installed.**
2.  **Install dependencies:**
    ```bash
    pip install customtkinter requests windows-toasts Pillow
    ```
3.  **Run the main script:**
    ```bash
    python main.py
    ```
    (Or whichever is the main executable script).
4.  **Configure Searches:** Use the application's interface to add and configure your desired search queries and filters.

## Disclaimer

This application interacts with the official Wallapop API. Users should be mindful of the API's terms of service and potential rate limits. The developers of this tool are not responsible for any misuse or actions taken against users by Wallapop as a result of using this application. Use responsibly.
