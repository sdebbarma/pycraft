
@demo
Feature: Payable Emi Alerts
	"""
	Area: Housing Loan; Set: Home Loan Calculator
	Feature: Calculate Payable Emi
	"""

	Scenario Outline: Invalid Loan Details
		Given User provides incorrect loan amount, rate and term
		
		@unit @dev @major
		Examples: Invalid loan amount
			| DEV 	| MAP 	| RUN 	| REFID 	| DESC									|
			| 		| 		|  		| B.TS2001	| Blank loan amount						|
			| 		|  		|  		| B.TS2002	| Negative loan amount					|

		When User wants to calculate payable emi
		Then System alerts user
