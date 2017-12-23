# Writeup

Answers to questions inline:

## 1. How long did you spend working on the problem? What did you find to be the most difficult part?

Day 1: About 3 hours for a single shot implementation.
Day 2: An hour for documentation and code organization.
Day 2: An hour for this writeup. (Commit not included in the `git log` below)

> git log
```
$ git log
commit 5ed6d0cfe57764dde8ff8d915b176913f449f0f9
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Thu Dec 21 12:45:20 2017 -0800

    Minor comments

commit dad0c5019ddc9e9f349bd94710dec3584a6c0193
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Thu Dec 21 12:40:02 2017 -0800

    Minor rename

commit a89bb0ca5b30f9fec876ccfc96d25287f4c3ba60
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Thu Dec 21 12:39:37 2017 -0800

    Documentation and Restructuring

commit 3f6e98117b5e38709e41237813e2a1a32822cf26
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Wed Dec 20 21:24:41 2017 -0800

    Complete first stab including manual test for small.csv

commit 9e89caa705107bf846184977d47a79d9e497995b
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Wed Dec 20 20:51:43 2017 -0800

    Basic LoanRequest class

commit 013207a7f266d28b1aef9359aeebca6701379a1a
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Wed Dec 20 20:22:59 2017 -0800

    Sort facilities_list by interest_rate to optimize yields

commit 58ca056964f3e667c879d5ed3ec2a1c56a6dbbb5
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Wed Dec 20 20:03:37 2017 -0800

    Facility Class with Covenants as attributes

commit 3dcd4920260c38e66010118ed170eef0c176830e
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Wed Dec 20 18:56:20 2017 -0800

    Data Import and inline Exploration (using debugger)

commit 48341d3b11ea9b3df13aac3451f26b45ac33a50d
Author: Manav Kataria <manavkataria.iitb@gmail.com>
Date:   Wed Dec 20 18:34:25 2017 -0800

    Initial Commit with problem statement and working data
```


## 2. How would you modify your data model or code to account for an eventual introduction of new, as­of­yet unknown types of covenants, beyond just maximum default likelihood and state restrictions?

I would:
1. Split `Facilities` and `Covenants` into independent classes  
1. Use Abstract Base Classes to lock in a minimal `Covenants` interface for future reuse and guidance and implement a specific one for this assignment

## 3. How would you architect your solution as a production service wherein new facilities can be introduced at arbitrary points in time. Assume these facilities become available by the finance team emailing your team and describing the addition with a new set of CSVs.

The system should be implemented as data-driven with configuration loaded in a master table `Facilities` in the database. Once a new `Facility` arrives as an email:
1. Automated Regression tests need to be triggered on the new csv to ensure they have valid format and data.
1. An Admin rest interface could be leveraged to add a new entry to the `Facilities` table.
1. A new entry could trigger (mechanisms: manual, REST API, message pushed into a distributed queue, etc.) reload of facilities given my current implementation.
-OR- For a streaming system `Facilities` data may be loaded at each loan request
1. Under certain cases, it would help to have the system run through a continuous integration and continuous deployment pipeline before the new data makes it to production

## 4. Your solution most likely simulates the streaming process by directly calling a method in your code to process the loans inside of a for loop. What would a REST API look like for this same service? Stakeholders using the API will need, at a minimum, to be able to request a loan be assigned to a facility, and read the funding status of a loan, as well as query the capacities remaining in facilities.

Few API interfaces:

`POST /loans`
Create a new loan request. Returns a loan `id`.

`GET /loans/`
`GET /loans/{LoanRequest:id}`
Gets all metadata for (all, or) a given loan, including origin `state`, `amount` requested, `interest_rate`, loan `status`, `assigned_facility`, etc. If `status=unassigned`, `assigned_facility` will be `None`

`POST /loan_facilities_requests/{LoanRequest:id}`
`POST /loan_facilities_requests/{Facility:id}/{LoanRequest:id}`
Request loan to be issued across (any facility, or) a specific facility. Returns yield, facility_id, loan assignment status.

`GET /loan_facilities_requests/`
`GET /loan_facilities_requests/?format=csv`
Generate & return facilities yield Report

`POST /facilities/`
Create a new facility

`GET /facilities/`
`GET /facilities/{Facility:id}`
Gets all metadata for (all, or) a given facility, including list of `covenants`, `current_expected_yield`, `current_balance_amount`, etc and a list of funded loans.

`PUT /facilities/`
Update a facility. Typically addition or deletion of a covenant. It might help to have version control for facilities given this update feature.

## 5. How might you improve your assignment algorithm if you were permitted to assign loans in batch rather than streaming? We are not looking for code here, but pseudo code or description of a revised algorithm appreciated.

Larger batch sizes leads to a more global optimization of a loans <> facilities assignment. Its akin to looking a bit into the future. Instead of using a Greedy algorithm a Dynamic programming algorithm like knapsack can be utilized to consume loans from various facilities. In lieu of time I would avoid providing details of a DP algorithm here. Happy to discuss this in detail over a call.

## 6. Because a number of facilities share the same interest rate, it’s possible that there are a number of equally appealing options by the algorithm we recommended you use (assigning to the cheapest facility). How might you tie­break facilities with equal interest rates, with the goal being to maximize the likelihood that future loans streaming in will be assignable to some facility?

One possible implementation is to analyze prior data to identify demand and supply trends and use them to (1)  predict a demographic demand trend (2) allocate appropriate facilities that are less likely to run dry for an overall optimization. For example, consider the following simple scenario:
1. Lending money to low-income states `S_low_income` usually runs out because many facilities `F_risk_averse` have covenants that might have banned those states `S_low_income`
1. All `F_risk_taking` facilities that did not ban `S_low_income` states have run out of lendable money. Their money was distributed to both `S_low_income` and `S_high_income` states.
1. Solution: Skew `F_risk_taking` facilities to assign loans to higher risk `S_low_income` states and utilize the under utilized `F_risk_averse` facilities for less risky `S_high_income` states.

# Possible Improvements:
1. Write positive and negative unit and functional test cases
1. Implement overwriting default configuration with using command line arguments
1. Move parsers to an input source specific class
1. Make class attributes private
1. Bake validation into issue_loan
