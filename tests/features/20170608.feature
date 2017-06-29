
@demo
Feature: Calculate Payable Emi
	"""
	Area: Housing Loan; Set: Home Loan Calculator
	Feature: Calculate Payable Emi
	"""

	Scenario Outline: Valid Loan Details
		Given User provides correct loan amount, rate and term
		
		@regression @test @minor
		Examples: Valid loan amount
			| DEV 	| MAP 	| RUN 	| REFID		| DESC							|
			| Y		| Y 	| 		| B.TS1001	| Loan amount > 1 crore			|
			| Y		| Y 	| 		| B.TS1002	| Loan amount < 50 thousands	|
		
		@sanity @test @default
		Examples: Valid loan term
			| DEV 	| MAP 	| RUN 	| REFID 	| DESC							|
			| Y		| Y		| 		| B.TS1003	| Minimum loan term				|
			| Y		|		|		| B.TS1004	| Maximum loan term				|
		
		When User wants to calculate payable emi
		Then System shows expected emi
		