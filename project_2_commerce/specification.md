# Website Specifications

## Models

- [x] The application must include at least three models **in addition** to the built-in `User` model:
  - [x] A model for auction listings
  - [x] A model for bids
  - [x] A model for comments
- [x] You may define additional models as needed.
- [x] You are free to choose appropriate fields and types for each model.

## Create Listing

- [x] Users should be able to create a new auction listing.
- [x] Listing form should allow input for:
  - [x] Title (text)
  - [x] Description (text)
  - [x] Starting bid (numeric)
  - [x] Image URL (optional)
  - [x] Category (optional, e.g., Fashion, Toys, Electronics, Home, etc.)

## Active Listings Page

- [x] The default route should display all currently active auction listings.
- [x] Each active listing should show:
  - [x] Title
  - [x] Description
  - [x] Current price (i.e., highest bid or starting bid)
  - [x] Image (if available)

## Listing Page

- [x] Clicking on a listing should lead to its individual listing page.
- [x] The listing page should display:
  - [x] All listing details
  - [x] Current price
  - [x] All comments associated with the listing

### Watchlist Features

- [x] If a user is signed in:
  - [x] They should be able to add the listing to their watchlist.
  - [x] If the listing is already in the watchlist, they should be able to remove it.

### Bidding Features

- [x] If a user is signed in:
  - [x] They should be able to place a bid on the listing.
  - [x] A bid is valid **only if**:
    - [x] It is at least as large as the starting bid.
    - [x] It is greater than any existing bids.
  - [x] If the bid is invalid, show an appropriate error message.

### Auction Closure

- [x] If the signed-in user is the creator of the listing:
  - [x] They should have the option to close the auction.
  - [x] Closing the auction:
    - [x] Declares the highest bidder as the winner.
    - [x] Marks the listing as no longer active.

### Post-Auction Display

- [x] If a user is signed in and viewing a closed listing:
  - [x] If they were the winning bidder, they should be informed that they won the auction.

### Comments

- [x] Signed-in users should be able to post comments on the listing.
- [x] All comments should be visible on the listing page.

## Watchlist Page

- [x] Signed-in users should be able to view a Watchlist page.
- [x] The Watchlist page should list all listings the user has added.
- [x] Clicking on a listing takes the user to the corresponding listing page.

## Categories

- [x] Users should be able to view all available listing categories.
- [x] Clicking on a category name should show:
  - [x] All **active** listings in that category.

## Django Admin Interface

- [x] Admins should be able to:
  - [x] View all listings, bids, and comments
  - [x] Add, edit, or delete listings, bids, and comments via the Django admin panel
